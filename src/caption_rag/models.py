"""Lazy Hugging Face model wrappers; importing the package does not require torch."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .data import open_rgb


class ModelBundle:
    def __init__(self, image_encoder: str, captioner: str, device: str = "auto"):
        try:
            import torch
            from transformers import BlipForConditionalGeneration, BlipProcessor, CLIPModel, CLIPProcessor
        except ImportError as exc:
            raise RuntimeError('Install model dependencies with: pip install -e ".[models]"') from exc
        self.torch = torch
        self.device = "cuda" if device == "auto" and torch.cuda.is_available() else ("cpu" if device == "auto" else device)
        self.clip_processor = CLIPProcessor.from_pretrained(image_encoder)
        self.clip = CLIPModel.from_pretrained(image_encoder).to(self.device).eval()
        self.blip_processor = BlipProcessor.from_pretrained(captioner)
        self.blip = BlipForConditionalGeneration.from_pretrained(captioner).to(self.device).eval()

    def image_embeddings(self, paths: list[str | Path], batch_size: int = 16) -> np.ndarray:
        vectors = []
        for start in range(0, len(paths), batch_size):
            images = [open_rgb(p) for p in paths[start:start + batch_size]]
            inputs = self.clip_processor(images=images, return_tensors="pt", padding=True).to(self.device)
            with self.torch.inference_mode():
                emb = self.clip(**inputs).image_embeds
            vectors.append(emb.cpu().numpy().astype("float32"))
        return np.concatenate(vectors) if vectors else np.empty((0, self.clip.config.projection_dim), dtype="float32")

    def image_text_scores(self, image_path: str | Path, texts: list[str]) -> np.ndarray:
        """Score candidate captions against the query image with the shared CLIP model."""
        if not texts:
            return np.empty((0,), dtype="float32")
        image = open_rgb(image_path)
        inputs = self.clip_processor(images=image, text=texts, return_tensors="pt",
                                     padding=True, truncation=True).to(self.device)
        with self.torch.inference_mode():
            scores = self.clip(**inputs).logits_per_image[0]
        return scores.float().cpu().numpy()

    def caption(self, path: str | Path, evidence: list[str] | None = None,
                max_new_tokens: int = 40, num_beams: int = 3) -> str:
        """BLIP caption baseline; evidence-conditioned mode prefixes retrieved caption hints."""
        image = open_rgb(path)
        prompt = ""
        if evidence:
            prompt = "Describe the image using only details supported by the image. Related captions may help: " + " ".join(evidence) + " Caption:"
        if prompt:
            inputs = self.blip_processor(images=image, text=prompt, return_tensors="pt").to(self.device)
        else:
            inputs = self.blip_processor(images=image, return_tensors="pt").to(self.device)
        with self.torch.inference_mode():
            output = self.blip.generate(**inputs, max_new_tokens=max_new_tokens,
                                        num_beams=num_beams, do_sample=False)
        return self.blip_processor.decode(output[0], skip_special_tokens=True).strip()
