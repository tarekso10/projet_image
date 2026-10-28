"""COCO caption/object descriptive statistics and plots."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def explore(instances_json: str, captions_json: str, output_dir: str) -> dict:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    instances = json.loads(Path(instances_json).read_text(encoding="utf-8"))
    captions = json.loads(Path(captions_json).read_text(encoding="utf-8"))
    category = {int(c["id"]): c["name"] for c in instances["categories"]}
    per_image = Counter(int(a["image_id"]) for a in instances["annotations"])
    object_counts = Counter(category[int(a["category_id"])] for a in instances["annotations"])
    caps_by_image: dict[int, list[str]] = {}
    for ann in captions["annotations"]:
        caps_by_image.setdefault(int(ann["image_id"]), []).append(ann["caption"])
    tokens = [re.findall(r"[\w']+", c.lower()) for vals in caps_by_image.values() for c in vals]
    lengths = [len(t) for t in tokens]
    vocab = Counter(t for sent in tokens for t in sent)

    pd.DataFrame(object_counts.most_common(50), columns=["class", "instances"]).to_csv(out / "top_objects.csv", index=False)
    pd.DataFrame([{"image_id": i, "object_count": n} for i, n in per_image.items()]).to_csv(out / "scene_complexity.csv", index=False)
    summary = {"images_with_instances": len(per_image), "mean_objects_per_annotated_image": sum(per_image.values()) / max(1, len(per_image)),
               "caption_count": sum(map(len, caps_by_image.values())), "mean_caption_words": sum(lengths) / max(1, len(lengths)),
               "vocabulary_size": len(vocab), "total_tokens": sum(vocab.values()),
               "top_object_classes": object_counts.most_common(50),
               "pos_distribution": "Not computed: requires optional language tagger; see README."}
    (out / "dataset_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    fig, ax = plt.subplots(figsize=(12, 5))
    top = object_counts.most_common(20)
    ax.bar([x[0] for x in top], [x[1] for x in top]); ax.tick_params(axis="x", rotation=65)
    ax.set_ylabel("COCO instances"); ax.set_title("Top 20 object classes")
    fig.tight_layout(); fig.savefig(out / "top_objects.png", dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 5)); ax.hist(lengths, bins=30)
    ax.set_xlabel("Words per caption"); ax.set_ylabel("Caption count"); ax.set_title("Caption length distribution")
    fig.tight_layout(); fig.savefig(out / "caption_lengths.png", dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 5)); ax.hist(list(per_image.values()), bins=30)
    ax.set_xlabel("Annotated objects per image"); ax.set_ylabel("Image count"); ax.set_title("Scene complexity")
    fig.tight_layout(); fig.savefig(out / "scene_complexity.png", dpi=160); plt.close(fig)
    return summary
