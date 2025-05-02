import json
import logging
from collections.abc import Callable
from pathlib import Path

import clip
import faiss
import numpy as np
import torch
from PIL import Image
from torch import Tensor

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class ImageSearchService:
    def __init__(self,
                 index_path: Path,
                 mapping_path: Path,
                 model_name: str,
                 device: str) -> None:
        self.device: str = device
        self.index_path: Path = index_path
        self.mapping_path: Path = mapping_path
        self.model: torch.nn.Module | None = None
        self.preprocess: Callable[[Image.Image], Tensor] | None = None
        self.index: faiss.Index | None = None
        self.image_paths: list[str] = []

        try:
            if self.model is None:
                self.model, self.preprocess = clip.load(
                    model_name, device=self.device)
                self.model.eval()

            self.index = faiss.read_index(str(self.index_path))
            with open(self.mapping_path, 'r', encoding='utf-8') as f:
                self.image_paths = json.load(f)

        except Exception as e:
            log.error(f"Error loading model or index: {e}")
            raise

    def search(self, query: Image.Image, top_k: int) -> tuple[list[str], list[float]]:
        try:
            query_rgb = query.convert("RGB")
            image_input = self.preprocess(
                query_rgb).unsqueeze(0).to(self.device)

            with torch.no_grad():
                query_embedding = self.model.encode_image(image_input)

            query_embedding_np = query_embedding.cpu().numpy().astype(np.float32)
            faiss.normalize_L2(query_embedding_np)
            distances, indices = self.index.search(query_embedding_np, top_k)

            results = []
            valid_distances = []
            if indices.size > 0:
                for i, idx in enumerate(indices[0]):
                    if idx != -1 and 0 <= idx < len(self.image_paths):
                        results.append(self.image_paths[idx])
                        valid_distances.append(distances[0][i])
            return results, valid_distances
        except Exception as e:
            log.error(f"Error during search: {e}")
            return [], []
