from pydantic import BaseModel, Field
from typing import Optional

class IngestRepoRequest(BaseModel):
    repo_url: str

class IngestLocalRequest(BaseModel):
    local_path: str

class IngestResponse(BaseModel):
    repo_id: str

class RepoOut(BaseModel):
    id: str
    repo_url: Optional[str]
    local_path: str
    default_branch: Optional[str]
    head_commit: Optional[str]

class FileOut(BaseModel):
    id: int
    path: str
    language: str
    size_bytes: int
    mtime_epoch: int

class CodeUnitOut(BaseModel):
    id: int
    unit_type: str
    name: str
    qualname: str
    signature: Optional[str]
    file_id: int
    start_line: int
    end_line: int
    language: str
    docstring: Optional[str]

class DeleteRepoResponse(BaseModel):
    repo_id: str
    deleted_metadata: bool
    deleted_clone: bool
    clone_path: Optional[str] = None

class PurgeResponse(BaseModel):
    deleted_metadata: int
    deleted_clones: bool

class EmbedRepoRequest(BaseModel):
    model: Optional[str] = None
    batch_size: int = Field(16, ge=1, le=256)
    force: bool = False

class EmbedRepoResponse(BaseModel):
    repo_id: str
    model: str
    dim: int
    created: int
    skipped: int

class EmbeddingStatsResponse(BaseModel):
    repo_id: str
    model: str
    count: int
    dim: Optional[int]

class UnitEmbeddingResponse(BaseModel):
    unit_id: int
    repo_id: str
    model: str
    dim: int
    content_hash: str
    vector_preview: list[float]
