from __future__ import annotations
import shutil
from pathlib import Path
from sqlalchemy import delete, select
from codesage.core.config import settings
from codesage.db.session import SessionLocal
from codesage.db.models import Repo, FileRecord, CodeUnit, CodeUnitEmbedding


def delete_repo(repo_id: str, delete_clone: bool = False) -> dict:
    deleted = {"repo_id": repo_id, "deleted_metadata": False, "deleted_clone": False, "clone_path": None}
    with SessionLocal() as db:
        repo = db.get(Repo, repo_id)
        if repo is None:
            return deleted
        db.execute(delete(CodeUnitEmbedding).where(CodeUnitEmbedding.repo_id==repo_id))
        db.execute(delete(CodeUnit).where(CodeUnit.repo_id==repo_id))
        db.execute(delete(FileRecord).where(FileRecord.repo_id==repo_id))
        db.execute(delete(Repo).where(Repo.id==repo_id))
        db.commit()
        deleted["deleted_metadata"] = True
        deleted["clone_path"] = repo.local_path

    if delete_clone and deleted["clone_path"]:
        p = Path(deleted["clone_path"]).resolve()
        clone_root = (settings.data_dir / settings.clone_dir_name).resolve()
        if str(p).startswith(str(clone_root)) and p.exists():
            shutil.rmtree(p, ignore_errors=True)
            deleted["deleted_clone"] = True
    return deleted


def purge_all(delete_clones: bool = False) -> dict:
    result = {"deleted_metadata": 0, "deleted_clones": False}
    with SessionLocal() as db:
        repo_ids = [r[0] for r in db.execute(select(Repo.id)).all()]
        db.execute(delete(CodeUnitEmbedding)); db.execute(delete(CodeUnit)); db.execute(delete(FileRecord)); db.execute(delete(Repo))
        db.commit()
        result["deleted_metadata"] = len(repo_ids)
    if delete_clones:
        clone_root = (settings.data_dir / settings.clone_dir_name).resolve()
        if clone_root.exists():
            shutil.rmtree(clone_root, ignore_errors=True)
        result["deleted_clones"] = True
    return result
