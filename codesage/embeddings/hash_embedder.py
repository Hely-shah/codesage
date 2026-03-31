from __future__ import annotations
import hashlib
import numpy as np
from codesage.embeddings.base import EmbeddingResult, l2_normalize

class HashEmbedder:
    def __init__(self, dim: int = 384, model_name: str = "hash-embedder-384"):
        self.dim = dim
        self.model_name = model_name

    def embed_texts(self, texts: list[str], batch_size: int = 64) -> EmbeddingResult:
        vecs = np.zeros((len(texts), self.dim), dtype=np.float32)
        for i, t in enumerate(texts):
            h = hashlib.sha256(t.encode("utf-8", errors="ignore")).digest()
            data = (h * ((self.dim * 4 // len(h)) + 1))[: self.dim * 4]
            arr = np.frombuffer(data, dtype=np.uint32).astype(np.float32)
            arr = (arr / np.float32(2**32 - 1)) * 2.0 - 1.0
            vecs[i] = arr
        return EmbeddingResult(vectors=l2_normalize(vecs), dim=self.dim)
