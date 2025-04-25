import numpy as np
import faiss
import json
import torch
import clip
import os
from io import BytesIO
from PIL import Image
from pathlib import Path
from app.core.config import settings


class ImageSearchService:
    def __init__(self,
                index_path: Path,
                mapping_path: Path,
                model_name: str,
                device: str | None):
        self.device = device
        self.index_path = index_path
        self.mapping_path = mapping_path
        self.model = None
        self.preprocess = None
        self.index = None
        self.image_paths = None
        
        try:
            if self.model is None:
                self.model, self.preprocess = clip.load(model_name, device=self.device)
                self.model.eval()
                
            self.index = faiss.read_index(str(self.index_path))
            with open(self.mapping_path, 'r', encoding='utf-8') as f:
                self.image_paths = json.load(f)
                
        except Exception as e:
            print(f"Error loading model or index: {e}")
            raise
    
    def search(self, query: str, top_k: int = 5) -> tuple[list[str], list[float]]:
        try:
            image_input = self.preprocess(query).unsqueeze(0).to(self.device)
            with torch.no_grad():
                query_embedding = self.model.encode_image(image_input).cpu().numpy().astype(np.float32)
            faiss.normalize_L2(query_embedding)
            distances, indices = self.index.search(query_embedding, top_k)
            
            results = []
            valid_distances = []
            if indices.size > 0:
                for i, idx in enumerate(indices[0]):
                    if idx != -1 and 0 <= idx < len(self.image_paths):
                        results.append(self.image_paths[idx])
                        valid_distances.append(distances[0][i])
            return results, valid_distances
        except Exception as e:
            return [], []