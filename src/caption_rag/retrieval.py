"""Deterministic dense retrieval over training captions and paired images."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence
import re

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


def compress_captions(candidates: list[dict], relevance_scores: np.ndarray,
                      max_captions: int = 4, max_words: int = 60) -> list[dict]:
    """Image-conditioned extractive compression with relevance ranking and redundancy removal.

    Candidates are short COCO captions. Keep the most image-relevant captions under a word
    budget; suppress near duplicates so repeated evidence does not dominate the prompt.
    """
    if len(candidates) != len(relevance_scores):
        raise ValueError("Each candidate caption must have one image-text relevance score")
    if max_captions < 1 or max_words < 1:
        raise ValueError("Compression budgets must be positive")
    order = np.argsort(-np.asarray(relevance_scores, dtype=np.float32), kind="stable")
    chosen: list[dict] = []
    chosen_tokens: list[set[str]] = []
    words_used = 0
    for i in order:
        item = candidates[int(i)]
        caption = item["caption"].strip()
        words = re.findall(r"\b[\w']+\b", caption)
        if not words:
            continue
        tokens = {w.casefold() for w in words}
        if any(len(tokens & prev) / max(1, len(tokens | prev)) >= 0.8 for prev in chosen_tokens):
            continue
        remaining = max_words - words_used
        if remaining <= 0:
            break
        if len(words) > remaining:
            if not chosen:
                caption = " ".join(words[:remaining])
                tokens = {w.casefold() for w in words[:remaining]}
            else:
                continue
        words_used += len(re.findall(r"\b[\w']+\b", caption))
        record = dict(item)
        record["caption"] = caption
        record["relevance"] = float(relevance_scores[int(i)])
        chosen.append(record)
        chosen_tokens.append(tokens)
        if len(chosen) >= max_captions:
            break
    return chosen
