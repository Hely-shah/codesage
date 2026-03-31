from __future__ import annotations
import numpy as np
from sqlalchemy import select, delete
from codesage.db.session import SessionLocal
from codesage.db.models import Repo, FileRecord, CodeUnit, CodeUnitEmbedding
from codesage.embeddings.registry import get_embedder
from codesage.embeddings.representation import build_representation


def _to_blob(vec: np.ndarray) -> bytes:
    return np.asarray(vec, dtype=np.float32).tobytes(order="C")

def _from_blob(blob: bytes, dim: int) -> np.ndarray:
    arr = np.frombuffer(blob, dtype=np.float32)
    return arr[:dim] if dim else arr


def embed_repo(repo_id: str, model: str | None = None, batch_size: int = 16, force: bool = False) -> dict:
    embedder = get_embedder(model)
    model_name = getattr(embedder, "model_name", model or "unknown")
    created = skipped = 0

    with SessionLocal() as db:
        repo = db.get(Repo, repo_id)
        if repo is None:
            raise ValueError("repo not found")

        file_map = {f.id: f.path for f in db.scalars(select(FileRecord).where(FileRecord.repo_id == repo_id)).all()}
        units = db.scalars(select(CodeUnit).where(CodeUnit.repo_id == repo_id).order_by(CodeUnit.id.asc())).all()
        if force:
            db.execute(delete(CodeUnitEmbedding).where(CodeUnitEmbedding.repo_id == repo_id, CodeUnitEmbedding.model == model_name))
            db.commit()

        texts=[]; candidates=[]
        for u in units:
            if not force:
                existing = db.scalars(select(CodeUnitEmbedding).where(CodeUnitEmbedding.unit_id==u.id, CodeUnitEmbedding.model==model_name, CodeUnitEmbedding.content_hash==u.content_hash).limit(1)).first()
                if existing:
                    skipped += 1
                    continue
            texts.append(build_representation(u, file_map.get(u.file_id)))
            candidates.append(u)

        if not candidates:
            return {"repo_id": repo_id, "model": model_name, "dim": 0, "created": 0, "skipped": skipped}

        emb = embedder.embed_texts(texts, batch_size=batch_size)
        for u, v in zip(candidates, emb.vectors):
            db.add(CodeUnitEmbedding(repo_id=repo_id, unit_id=u.id, model=model_name, dim=emb.dim, vector=_to_blob(v), content_hash=u.content_hash))
            created += 1
        db.commit()

    return {"repo_id": repo_id, "model": model_name, "dim": emb.dim, "created": created, "skipped": skipped}


def embedding_stats(repo_id: str, model: str | None = None) -> dict:
    embedder = get_embedder(model)
    model_name = getattr(embedder, "model_name", model or "unknown")
    with SessionLocal() as db:
        rows = db.scalars(select(CodeUnitEmbedding).where(CodeUnitEmbedding.repo_id==repo_id, CodeUnitEmbedding.model==model_name)).all()
        return {"repo_id": repo_id, "model": model_name, "count": len(rows), "dim": (rows[0].dim if rows else None)}


def get_unit_embedding(unit_id: int, model: str | None = None) -> dict:
    embedder = get_embedder(model)
    model_name = getattr(embedder, "model_name", model or "unknown")
    with SessionLocal() as db:
        emb = db.scalars(select(CodeUnitEmbedding).where(CodeUnitEmbedding.unit_id==unit_id, CodeUnitEmbedding.model==model_name).order_by(CodeUnitEmbedding.created_at.desc()).limit(1)).first()
        if emb is None:
            raise ValueError("embedding not found")
        vec = _from_blob(emb.vector, emb.dim)
        return {"unit_id": unit_id, "repo_id": emb.repo_id, "model": emb.model, "dim": emb.dim, "content_hash": emb.content_hash, "vector_preview": vec[:min(10, vec.size)].tolist()}
