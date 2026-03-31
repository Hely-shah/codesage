from __future__ import annotations
from codesage.embeddings.hash_embedder import HashEmbedder

def get_embedder(model: str | None):
    if model is None or model.startswith("hash-"):
        return HashEmbedder()
    try:
        from codesage.embeddings.hf_embedder import HFEmbedder
        return HFEmbedder(model_name=model)
    except Exception:
        return HashEmbedder()
