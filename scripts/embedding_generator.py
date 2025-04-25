import faiss
import torch
import json
import sys
import clip
import numpy as np
from faiss import write_index
from PIL import Image
from tqdm import tqdm
from pathlib import Path
app_route = Path(__file__).resolve().parent.parent
sys.path.append(str(app_route))
from app.core.config import settings


class GenerateEmbedding:
    def __init__(self,
                image_dir: Path,
                index_output_dir: Path,
                index_file_dir: Path,
                mapping_file_dir: Path,
                model_name: str,
                device: str = None):
        self.image_dir = image_dir
        self.index_output_dir = index_output_dir
        self.index_file_dir = index_file_dir
        self.mapping_file_dir = mapping_file_dir
        self.model_name = model_name
        self.device = device
        self.model = None
        self.preprocess = None
        
    def _load_model(self):
        try:
            self.model, self.preprocess = clip.load(self.model_name,
                                                    device=self.device)
            self.model.eval()
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
        
    def _get_image_files(self) -> list[Path]:
        image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        image_files = [
            _ for _ in self.image_dir.rglob("*")
            if _.is_file() and _.suffix.lower() in image_extensions
        ]
        if not image_files:
            print("No images found.")
        return image_files
    
    def _process_images(self, image_files: list[Path]) -> tuple:
        all_embeddings = []
        all_image_paths = []
        dimension = None
        for image_path in tqdm(image_files, desc="Processing images", unit="image", ncols=100):
            try:
                image = Image.open(image_path).convert("RGB")
                image_input = self.preprocess(image).unsqueeze(0).to(self.device)
                with torch.no_grad():
                    embedding = self.model.encode_image(image_input)
                embedding /= embedding.norm(dim=-1, keepdim=True)
                np_embedding = embedding.cpu().numpy()[0].astype(np.float32)
                
                all_embeddings.append(np_embedding)
                all_image_paths.append(str(image_path.resolve()))
                if dimension is None:
                    dimension = np_embedding.shape[0]
            except Exception as e:
                tqdm.write(f"\nWarning: Failed to process image {e}")
                continue
        return all_embeddings, all_image_paths, dimension
    
    def _create_faiss_index(self, embeddings_np: np.ndarray, dimension: int) -> faiss.Index | None:
        try: 
            index = faiss.IndexFlatIP(dimension)
            index.add(embeddings_np)
            if index.ntotal != len(embeddings_np):
                print("Indexing failed.")
            return index
        except Exception as e:
            return None
        
    def _save_index(self, index: faiss.Index, image_paths: list[str]) -> bool:
        save_status = True
        try:
            write_index(index, str(self.index_file_dir))
        except Exception as e:
            print(f"Error saving index: {e}")
            save_status = False
        
        try:
            with open(self.mapping_file_dir, 'w', encoding='utf-8') as f:
                json.dump(image_paths, f, indent=4)
        except IOError as e:
            print(f"Error saving mapping file: {e}")
            save_status = False
        
        return save_status
                
    def generate_embeddings(self):
        try:
            self._load_model()
            image_files = self._get_image_files()
            
            if not image_files:
                print("No images found.")
                return
            
            results = self._process_images(image_files)
            all_embeddings, all_image_paths, dimension = results
            
            if not all_embeddings or dimension is None:
                print("No valid embeddings found.")
                return
            
            all_embeddings_np = np.array(all_embeddings).astype(np.float32)
            index = self._create_faiss_index(all_embeddings_np, dimension)
            
            if index is None:
                print("Failed to create FAISS index.")
                return
            
            save_status = self._save_index(index, all_image_paths)
            
            if save_status:
                print("Index and mapping file saved successfully.")
        except Exception as e:
            print(f"Error during embedding generation: {e}")

if __name__ == "__main__":
    indexer = GenerateEmbedding(
        image_dir=settings.STATIC_IMAGE_PATH,
        index_output_dir=settings.INDEX_FAISS_PATH,
        index_file_dir=settings.INDEX_FAISS_PATH,
        mapping_file_dir=settings.MAPPING_ROUTES_PATH,
        model_name=settings.CLIP_MODEL_NAME,
        device=settings.DEVICE
    )
    indexer.generate_embeddings()