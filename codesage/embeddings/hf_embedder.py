from __future__ import annotations
import numpy as np
from codesage.embeddings.base import EmbeddingResult, l2_normalize
from codesage.core.config import settings

class HFEmbedder:
    def __init__(self, model_name: str | None = None, max_length: int | None = None, device: str | None = None):
        self.model_name = model_name or settings.embedding_model
        self.max_length = max_length or settings.embedding_max_length
        self.device = device
        import torch
        from transformers import AutoTokenizer, AutoModel
        self._torch = torch
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self._model = AutoModel.from_pretrained(self.model_name)
        if self.device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._model.to(self.device)
        self._model.eval()

    def embed_texts(self, texts: list[str], batch_size: int = 8) -> EmbeddingResult:
        torch = self._torch
        vecs = []
        with torch.no_grad():
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i+batch_size]
                enc = self._tokenizer(batch, padding=True, truncation=True, max_length=self.max_length, return_tensors="pt")
                enc = {k: v.to(self.device) for k, v in enc.items()}
                out = self._model(**enc)
                last = out.last_hidden_state
                attn = enc.get("attention_mask")
                mask = attn.unsqueeze(-1).expand(last.size()).float()
                pooled = (last * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1e-9)
                vecs.append(pooled.detach().cpu().numpy().astype(np.float32))
        mat = np.vstack(vecs)
        return EmbeddingResult(vectors=l2_normalize(mat), dim=int(mat.shape[1]))
