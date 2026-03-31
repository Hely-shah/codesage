from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol
import numpy as np

@dataclass
class EmbeddingResult:
    vectors: np.ndarray
    dim: int

class Embedder(Protocol):
    model_name: str
    def embed_texts(self, texts: list[str], batch_size: int = 16) -> EmbeddingResult: ...

def l2_normalize(x: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    denom = np.linalg.norm(x, axis=1, keepdims=True)
    denom = np.maximum(denom, eps)
    return x / denom
