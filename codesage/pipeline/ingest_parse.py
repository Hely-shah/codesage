from __future__ import annotations
import hashlib
from pathlib import Path
from sqlalchemy import delete
from codesage.core.config import settings
from codesage.db.session import SessionLocal
from codesage.db.models import Repo, FileRecord, CodeUnit, CodeUnitEmbedding
from codesage.db.init_db import init_db
from codesage.ingestion.git_client import clone_or_update
from codesage.ingestion.file_walker import walk_repo
from codesage.parsing.registry import get_parser


def _hash_content(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="ignore")).hexdigest()


def ingest_repo(repo_url: str) -> str:
    init_db()
    clone_root = settings.data_dir / settings.clone_dir_name
    clone = clone_or_update(repo_url, clone_root)
    with SessionLocal() as db:
        repo = db.get(Repo, clone.repo_id)
        if repo is None:
            repo = Repo(id=clone.repo_id, repo_url=repo_url, local_path=str(clone.local_path), default_branch=clone.default_branch, head_commit=clone.head_commit)
            db.add(repo)
        else:
            repo.repo_url=repo_url; repo.local_path=str(clone.local_path); repo.default_branch=clone.default_branch; repo.head_commit=clone.head_commit

        db.execute(delete(CodeUnitEmbedding).where(CodeUnitEmbedding.repo_id==clone.repo_id))
        db.execute(delete(CodeUnit).where(CodeUnit.repo_id==clone.repo_id))
        db.execute(delete(FileRecord).where(FileRecord.repo_id==clone.repo_id))
        db.commit()

        for f in walk_repo(clone.local_path):
            fr = FileRecord(repo_id=clone.repo_id, path=f.rel_path, language=f.language, size_bytes=f.size_bytes, mtime_epoch=f.mtime_epoch)
            db.add(fr); db.flush()
            parser = get_parser(f.language)
            if parser is None: continue
            text = f.path.read_text(encoding="utf-8", errors="ignore")
            for u in parser.parse(text, f.rel_path):
                db.add(CodeUnit(repo_id=clone.repo_id, file_id=fr.id, unit_type=u.unit_type, name=u.name, qualname=u.qualname, signature=u.signature,
                                start_line=u.start_line, end_line=u.end_line, language=f.language, docstring=u.docstring, code=u.code, content_hash=_hash_content(u.code)))
        db.commit()
    return clone.repo_id


def ingest_local_path(local_path: str) -> str:
    init_db()
    root = Path(local_path).resolve()
    repo_id = hashlib.sha1(str(root).encode("utf-8")).hexdigest()
    with SessionLocal() as db:
        repo = db.get(Repo, repo_id)
        if repo is None:
            repo = Repo(id=repo_id, repo_url=None, local_path=str(root), default_branch=None, head_commit=None)
            db.add(repo)
        else:
            repo.local_path=str(root)
        db.execute(delete(CodeUnitEmbedding).where(CodeUnitEmbedding.repo_id==repo_id))
        db.execute(delete(CodeUnit).where(CodeUnit.repo_id==repo_id))
        db.execute(delete(FileRecord).where(FileRecord.repo_id==repo_id))
        db.commit()

        for f in walk_repo(root):
            fr = FileRecord(repo_id=repo_id, path=f.rel_path, language=f.language, size_bytes=f.size_bytes, mtime_epoch=f.mtime_epoch)
            db.add(fr); db.flush()
            parser = get_parser(f.language)
            if parser is None: continue
            text = f.path.read_text(encoding="utf-8", errors="ignore")
            for u in parser.parse(text, f.rel_path):
                db.add(CodeUnit(repo_id=repo_id, file_id=fr.id, unit_type=u.unit_type, name=u.name, qualname=u.qualname, signature=u.signature,
                                start_line=u.start_line, end_line=u.end_line, language=f.language, docstring=u.docstring, code=u.code, content_hash=_hash_content(u.code)))
        db.commit()
    return repo_id
