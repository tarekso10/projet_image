"""Lazy Hugging Face model wrappers; importing the package does not require torch."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .data import open_rgb


class ModelBundle:
    def __init__(self, image_encoder: str, captioner: str, text_encoder: str, device: str = "auto"):
        try:
            import torch
            from transformers import BlipForConditionalGeneration, BlipProcessor, CLIPModel, CLIPProcessor
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError('Install model dependencies with: pip install -e ".[models]"') from exc
        self.torch = torch
        self.device = "cuda" if device == "auto" and torch.cuda.is_available() else ("cpu" if device == "auto" else device)
        self.clip_processor = CLIPProcessor.from_pretrained(image_encoder)
        self.clip = CLIPModel.from_pretrained(image_encoder).to(self.device).eval()
        self.blip_processor = BlipProcessor.from_pretrained(captioner)
        self.blip = BlipForConditionalGeneration.from_pretrained(captioner).to(self.device).eval()
        self.text = SentenceTransformer(text_encoder, device=self.device)

    def image_embeddings(self, paths: list[str | Path], batch_size: int = 16) -> np.ndarray:
        vectors = []
        for start in range(0, len(paths), batch_size):
            images = [open_rgb(p) for p in paths[start:start + batch_size]]
            inputs = self.clip_processor(images=images, return_tensors="pt", padding=True).to(self.device)
            with self.torch.inference_mode():
                emb = self.clip.get_image_features(**inputs)
            vectors.append(emb.cpu().numpy().astype("float32"))
        return np.concatenate(vectors) if vectors else np.empty((0, self.clip.config.projection_dim), dtype="float32")

    def text_embeddings(self, texts: list[str], batch_size: int = 64) -> np.ndarray:
        return self.text.encode(texts, batch_size=batch_size, normalize_embeddings=True,
                                convert_to_numpy=True, show_progress_bar=True).astype("float32")

    def caption(self, path: str | Path, evidence: list[str] | None = None,
                max_new_tokens: int = 40, num_beams: int = 3) -> str:
        """BLIP caption baseline; evidence-conditioned mode prefixes retrieved caption hints."""
        image = open_rgb(path)
        prompt = ""
        if evidence:
            prompt = "Describe the image using this related visual evidence when relevant: " + " ".join(evidence[:3]) + " Caption:"
        if prompt:
            inputs = self.blip_processor(images=image, text=prompt, return_tensors="pt").to(self.device)
        else:
            inputs = self.blip_processor(images=image, return_tensors="pt").to(self.device)
        with self.torch.inference_mode():
            output = self.blip.generate(**inputs, max_new_tokens=max_new_tokens,
                                        num_beams=num_beams, do_sample=False)
        return self.blip_processor.decode(output[0], skip_special_tokens=True).strip()
