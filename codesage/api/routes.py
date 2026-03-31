from __future__ import annotations
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from codesage.api.schemas import (
    IngestRepoRequest, IngestLocalRequest, IngestResponse,
    RepoOut, FileOut, CodeUnitOut,
    DeleteRepoResponse, PurgeResponse,
    EmbedRepoRequest, EmbedRepoResponse,
    EmbeddingStatsResponse, UnitEmbeddingResponse,
)
from codesage.pipeline.ingest_parse import ingest_repo, ingest_local_path
from codesage.pipeline.delete_repo import delete_repo, purge_all
from codesage.pipeline.embed_repo import embed_repo, embedding_stats, get_unit_embedding
from codesage.db.session import SessionLocal
from codesage.db.models import Repo, FileRecord, CodeUnit

router = APIRouter()

@router.post('/ingest/repo', response_model=IngestResponse)
def ingest_repo_endpoint(req: IngestRepoRequest):
    try:
        return IngestResponse(repo_id=ingest_repo(req.repo_url))
    except Exception as e:
        raise HTTPException(400, str(e))

@router.post('/ingest/local', response_model=IngestResponse)
def ingest_local_endpoint(req: IngestLocalRequest):
    try:
        return IngestResponse(repo_id=ingest_local_path(req.local_path))
    except Exception as e:
        raise HTTPException(400, str(e))

@router.get('/repos', response_model=list[RepoOut])
def list_repos():
    with SessionLocal() as db:
        rows = db.scalars(select(Repo).order_by(Repo.created_at.desc())).all()
        return [RepoOut(id=r.id, repo_url=r.repo_url, local_path=r.local_path, default_branch=r.default_branch, head_commit=r.head_commit) for r in rows]

@router.get('/repos/{repo_id}', response_model=RepoOut)
def repo_details(repo_id: str):
    with SessionLocal() as db:
        r = db.get(Repo, repo_id)
        if not r:
            raise HTTPException(404, 'repo not found')
        return RepoOut(id=r.id, repo_url=r.repo_url, local_path=r.local_path, default_branch=r.default_branch, head_commit=r.head_commit)

@router.get('/repos/{repo_id}/files', response_model=list[FileOut])
def list_files(repo_id: str, language: str | None = None, limit: int = Query(200, ge=1, le=2000)):
    with SessionLocal() as db:
        stmt = select(FileRecord).where(FileRecord.repo_id==repo_id)
        if language:
            stmt = stmt.where(FileRecord.language==language)
        rows = db.scalars(stmt.order_by(FileRecord.path.asc()).limit(limit)).all()
        return [FileOut(id=f.id, path=f.path, language=f.language, size_bytes=f.size_bytes, mtime_epoch=f.mtime_epoch) for f in rows]

@router.get('/repos/{repo_id}/units', response_model=list[CodeUnitOut])
def list_units(repo_id: str, type: str | None = None, q: str | None = None, limit: int = Query(200, ge=1, le=2000)):
    with SessionLocal() as db:
        stmt = select(CodeUnit).where(CodeUnit.repo_id==repo_id)
        if type:
            stmt = stmt.where(CodeUnit.unit_type==type)
        if q:
            like=f"%{q}%"; stmt = stmt.where((CodeUnit.name.like(like)) | (CodeUnit.qualname.like(like)))
        rows = db.scalars(stmt.order_by(CodeUnit.file_id.asc(), CodeUnit.start_line.asc()).limit(limit)).all()
        return [CodeUnitOut(id=u.id, unit_type=u.unit_type, name=u.name, qualname=u.qualname, signature=u.signature, file_id=u.file_id, start_line=u.start_line, end_line=u.end_line, language=u.language, docstring=u.docstring) for u in rows]

@router.get('/units/{unit_id}')
def get_unit(unit_id: int):
    with SessionLocal() as db:
        u = db.get(CodeUnit, unit_id)
        if not u:
            raise HTTPException(404, 'unit not found')
        return {"id": u.id, "repo_id": u.repo_id, "file_id": u.file_id, "unit_type": u.unit_type, "name": u.name, "qualname": u.qualname, "signature": u.signature, "start_line": u.start_line, "end_line": u.end_line, "language": u.language, "docstring": u.docstring, "code": u.code}

@router.post('/embed/repos/{repo_id}', response_model=EmbedRepoResponse)
def embed_repo_endpoint(repo_id: str, req: EmbedRepoRequest):
    try:
        return EmbedRepoResponse(**embed_repo(repo_id, model=req.model, batch_size=req.batch_size, force=req.force))
    except Exception as e:
        raise HTTPException(400, str(e))

@router.get('/repos/{repo_id}/embeddings', response_model=EmbeddingStatsResponse)
def embedding_stats_endpoint(repo_id: str, model: str | None = None):
    try:
        return EmbeddingStatsResponse(**embedding_stats(repo_id, model=model))
    except Exception as e:
        raise HTTPException(400, str(e))

@router.get('/units/{unit_id}/embedding', response_model=UnitEmbeddingResponse)
def unit_embedding_endpoint(unit_id: int, model: str | None = None):
    try:
        return UnitEmbeddingResponse(**get_unit_embedding(unit_id, model=model))
    except Exception as e:
        raise HTTPException(404, str(e))

@router.delete('/repos/{repo_id}', response_model=DeleteRepoResponse)
def delete_repo_endpoint(repo_id: str, delete_clone: bool = Query(False)):
    return DeleteRepoResponse(**delete_repo(repo_id, delete_clone=delete_clone))

@router.delete('/repos', response_model=PurgeResponse)
def purge_all_endpoint(delete_clones: bool = Query(False)):
    return PurgeResponse(**purge_all(delete_clones=delete_clones))
