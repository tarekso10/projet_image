"""Command line interface for preparing data and running caption experiments."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from .data import load_coco, validate_splits, write_jsonl
from .metrics import caption_metrics, caption_metrics_per_image, paired_comparison
from .models import ModelBundle
from .retrieval import DenseIndex


def _config(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def prepare(args: argparse.Namespace) -> None:
    cfg = _config(args.config)
    root = Path(cfg["data"]["root"])
    train = load_coco(args.train_annotations, args.train_images)
    val = load_coco(args.val_annotations, args.val_images)
    train = train[train.captions.map(len).eq(5)].copy()
    val = val[val.captions.map(len).eq(5)].copy()
    random.Random(cfg["project"]["seed"]).shuffle(train_ids := train.image_id.tolist())
    n_train = min(args.train_count or cfg["data"]["train_images"], len(train_ids))
    train_ids = set(train_ids[:n_train])
    train = train[train.image_id.isin(train_ids)]

    # The assignment's common split is 100 validation + 100 test images; shared course IDs
    # override deterministic sampling when the instructors provide them.
    val_ids_path = Path(cfg["data"]["validation_ids"])
    test_ids_path = Path(cfg["data"]["test_ids"])
    def ids(path: Path, count: int, salt: int) -> set[int]:
        if path.is_file():
            return {int(s) for s in path.read_text(encoding="utf-8").splitlines() if s.strip() and not s.startswith("#")}
        candidates = sorted(val.image_id.astype(int).tolist())
        random.Random(cfg["project"]["seed"] + salt).shuffle(candidates)
        return set(candidates[:count])
    val_ids = ids(val_ids_path, cfg["data"]["validation_images"], 1)
    test_ids = ids(test_ids_path, cfg["data"]["test_images"], 2)
    if val_ids & test_ids:
        # Without instructor-provided IDs, make deterministic disjoint subsets.
        if not (val_ids_path.is_file() or test_ids_path.is_file()):
            test_ids -= val_ids
            remaining = [i for i in sorted(val.image_id.astype(int)) if i not in val_ids]
            random.Random(cfg["project"]["seed"] + 3).shuffle(remaining)
            test_ids.update(remaining[:cfg["data"]["test_images"]])
        else:
            raise ValueError("Instructor-provided validation and test IDs overlap")
    validation = val[val.image_id.isin(val_ids)]
    test = val[val.image_id.isin(test_ids)]
    sizes = validate_splits(train, validation, test)
    out = root / "processed"
    for name, frame in (("knowledge", train), ("validation", validation), ("test", test)):
        rows = frame.to_dict(orient="records")
        write_jsonl(rows, out / f"{name}.jsonl")
    (root / "splits").mkdir(parents=True, exist_ok=True)
    for name, frame in (("validation", validation), ("test", test)):
        (root / "splits" / f"{name}_ids.txt").write_text(
            "\n".join(map(str, sorted(frame.image_id.astype(int)))) + "\n", encoding="utf-8")
    (out / "split_audit.json").write_text(json.dumps({"sizes": sizes, "overlap": False,
        "note": "Validation/test IDs are local deterministic substitutes unless course IDs were supplied."}, indent=2), encoding="utf-8")
    print(json.dumps(sizes, indent=2))


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def run(args: argparse.Namespace) -> None:
    cfg = _config(args.config)
    root = Path(cfg["data"]["root"])
    knowledge = _read_jsonl(root / "processed" / "knowledge.jsonl")
    test = _read_jsonl(root / "processed" / "test.jsonl")
    model = ModelBundle(cfg["models"]["image_encoder"], cfg["models"]["captioner"],
                        cfg["models"]["text_encoder"], cfg["models"]["device"])
    out = Path(cfg["project"]["output_dir"])
    out.mkdir(parents=True, exist_ok=True)
    # Image-to-image retrieval must rank distinct images, not let one image occupy all top-k
    # slots through its five separately indexed captions. Keep its five captions together.
    train_vec = model.image_embeddings([r["image_path"] for r in knowledge], args.batch_size)
    query_vec = model.image_embeddings([r["image_path"] for r in test], args.batch_size)
    np.save(out / "knowledge_image_embeddings.npy", train_vec)
    index = DenseIndex.build(train_vec, [r["image_id"] for r in knowledge],
                             [" | ".join(r["captions"]) for r in knowledge])
    result_rows = []
    for row, query in zip(test, query_vec):
        baseline = model.caption(row["image_path"], max_new_tokens=cfg["generation"]["max_new_tokens"],
                                 num_beams=cfg["generation"]["num_beams"])
        hits = index.search(query, top_k=cfg["retrieval"]["top_k"], exclude_image_id=row["image_id"])
        rag = model.caption(row["image_path"], [h["caption"] for h in hits],
                            max_new_tokens=cfg["generation"]["max_new_tokens"],
                            num_beams=cfg["generation"]["num_beams"])
        result_rows.extend([
            {"image_id": row["image_id"], "method": "baseline", "caption": baseline,
             "confidence": None, "references": row["captions"], "retrieved_ids": []},
            {"image_id": row["image_id"], "method": "dense_rag", "caption": rag,
             "confidence": None, "references": row["captions"],
             "retrieved_ids": [h["image_id"] for h in hits], "retrieval_scores": [h["score"] for h in hits]},
        ])
    write_jsonl(result_rows, out / "captions.jsonl")
    method_metrics = {}
    for method in ("baseline", "dense_rag"):
        rows = [r for r in result_rows if r["method"] == method]
        scores = caption_metrics([r["caption"] for r in rows], [r["references"] for r in rows])
        method_metrics[method] = caption_metrics_per_image([r["caption"] for r in rows],
                                                            [r["references"] for r in rows])
        (out / f"metrics_{method}.json").write_text(json.dumps(scores, indent=2), encoding="utf-8")
    comparisons = {metric: paired_comparison(method_metrics["baseline"][metric],
                                              method_metrics["dense_rag"][metric],
                                              comparisons=5)
                   for metric in method_metrics["baseline"]}
    (out / "paired_statistics.json").write_text(json.dumps(comparisons, indent=2), encoding="utf-8")
    print(f"Wrote {len(result_rows)} caption rows and aggregate metrics to {out}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="caption-rag")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare", help="create leakage-checked COCO splits")
    p.add_argument("--config", default="config/default.yaml")
    p.add_argument("--train-annotations", required=True)
    p.add_argument("--train-images", required=True)
    p.add_argument("--val-annotations", required=True)
    p.add_argument("--val-images", required=True)
    p.add_argument("--train-count", type=int)
    p.set_defaults(func=prepare)
    r = sub.add_parser("run", help="run BLIP baseline and dense image-to-image RAG")
    r.add_argument("--config", default="config/default.yaml")
    r.add_argument("--batch-size", type=int, default=16)
    r.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
