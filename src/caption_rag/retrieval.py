"""Deterministic dense retrieval over training captions and paired images."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass
class DenseIndex:
    vectors: np.ndarray
    image_ids: np.ndarray
    captions: list[str]

    @classmethod
    def build(cls, vectors: np.ndarray, image_ids: Sequence[int], captions: Sequence[str]) -> "DenseIndex":
        vectors = np.asarray(vectors, dtype=np.float32)
        if vectors.ndim != 2 or len(vectors) != len(image_ids) or len(vectors) != len(captions):
            raise ValueError("vectors, image_ids, and captions must have matching lengths")
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        vectors = vectors / np.maximum(norms, 1e-12)
        return cls(vectors, np.asarray(image_ids, dtype=np.int64), list(captions))

    def search(self, query: np.ndarray, top_k: int = 5,
               exclude_image_id: int | None = None) -> list[dict]:
        """Cosine search with mandatory self-match exclusion for evaluation images."""
        if top_k < 1:
            raise ValueError("top_k must be positive")
        q = np.asarray(query, dtype=np.float32).reshape(-1)
        if q.shape[0] != self.vectors.shape[1]:
            raise ValueError(f"query dimension {q.shape[0]} != index dimension {self.vectors.shape[1]}")
        q /= max(float(np.linalg.norm(q)), 1e-12)
        scores = self.vectors @ q
        if exclude_image_id is not None:
            scores[self.image_ids == int(exclude_image_id)] = -np.inf
        count = min(top_k, int(np.isfinite(scores).sum()))
        if count == 0:
            return []
        idx = np.argpartition(scores, -count)[-count:]
        idx = idx[np.argsort(scores[idx])[::-1]]
        return [{"image_id": int(self.image_ids[i]), "caption": self.captions[i],
                 "score": float(scores[i])} for i in idx]
