"""COCO data loading, split checks, and leakage safeguards."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
from PIL import Image, ImageOps


def read_id_file(path: str | Path | None) -> set[int]:
    if path is None or not Path(path).exists():
        return set()
    return {int(line.strip()) for line in Path(path).read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")}


def load_coco(annotation_file: str | Path, image_dir: str | Path) -> pd.DataFrame:
    """Return one row per COCO image, preserving all five raw reference captions."""
    payload: dict[str, Any] = json.loads(Path(annotation_file).read_text(encoding="utf-8"))
    captions: dict[int, list[str]] = {}
    for ann in payload.get("annotations", []):
        captions.setdefault(int(ann["image_id"]), []).append(str(ann["caption"]))
    rows = []
    for image in payload.get("images", []):
        image_id = int(image["id"])
        rows.append({"image_id": image_id, "file_name": image["file_name"],
                     "image_path": str(Path(image_dir) / image["file_name"]),
                     "captions": captions.get(image_id, [])})
    return pd.DataFrame(rows)


def validate_splits(knowledge: pd.DataFrame, validation: pd.DataFrame,
                    test: pd.DataFrame) -> dict[str, int]:
    """Fail closed on ID overlap, duplicate IDs, missing files, or non-five-caption rows."""
    frames = {"knowledge": knowledge, "validation": validation, "test": test}
    sets: dict[str, set[int]] = {}
    for name, frame in frames.items():
        if frame["image_id"].duplicated().any():
            raise ValueError(f"Duplicate image IDs in {name} split")
        sets[name] = set(frame["image_id"].astype(int))
        if "image_path" in frame:
            missing = [p for p in frame["image_path"] if not Path(p).is_file()]
            if missing:
                raise FileNotFoundError(f"{name}: {len(missing)} image files are missing; e.g. {missing[0]}")
        if "captions" in frame:
            bad = frame["captions"].map(len).ne(5)
            if bad.any():
                raise ValueError(f"{name}: expected exactly five captions per image; {int(bad.sum())} violations")
    for left, right in (("knowledge", "validation"), ("knowledge", "test"), ("validation", "test")):
        overlap = sets[left] & sets[right]
        if overlap:
            raise ValueError(f"Split leakage between {left} and {right}: {len(overlap)} IDs (e.g. {min(overlap)})")
    return {name: len(ids) for name, ids in sets.items()}


def open_rgb(path: str | Path) -> Image.Image:
    """Open an image, apply EXIF orientation, and convert to RGB."""
    with Image.open(path) as im:
        return ImageOps.exif_transpose(im).convert("RGB")


def write_jsonl(rows: list[dict[str, Any]], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
