from __future__ import annotations
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, UniqueConstraint, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from codesage.db.session import Base

class Repo(Base):
    __tablename__ = "repos"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    repo_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    local_path: Mapped[str] = mapped_column(String(2048), nullable=False)
    default_branch: Mapped[str | None] = mapped_column(String(255), nullable=True)
    head_commit: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    files: Mapped[list[FileRecord]] = relationship(back_populates="repo", cascade="all, delete-orphan")
    units: Mapped[list[CodeUnit]] = relationship(back_populates="repo", cascade="all, delete-orphan")

class FileRecord(Base):
    __tablename__ = "files"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    repo_id: Mapped[str] = mapped_column(ForeignKey("repos.id"), index=True)
    path: Mapped[str] = mapped_column(String(2048), index=True)
    language: Mapped[str] = mapped_column(String(64), index=True)
    size_bytes: Mapped[int] = mapped_column(Integer)
    mtime_epoch: Mapped[int] = mapped_column(Integer)
    repo: Mapped[Repo] = relationship(back_populates="files")
    units: Mapped[list[CodeUnit]] = relationship(back_populates="file", cascade="all, delete-orphan")
    __table_args__ = (UniqueConstraint("repo_id", "path", name="uq_repo_file"),)

class CodeUnit(Base):
    __tablename__ = "code_units"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    repo_id: Mapped[str] = mapped_column(ForeignKey("repos.id"), index=True)
    file_id: Mapped[int] = mapped_column(ForeignKey("files.id"), index=True)
    unit_type: Mapped[str] = mapped_column(String(32), index=True)
    name: Mapped[str] = mapped_column(String(512), index=True)
    qualname: Mapped[str] = mapped_column(String(1024), index=True)
    signature: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    start_line: Mapped[int] = mapped_column(Integer)
    end_line: Mapped[int] = mapped_column(Integer)
    language: Mapped[str] = mapped_column(String(64), index=True)
    docstring: Mapped[str | None] = mapped_column(Text, nullable=True)
    code: Mapped[str] = mapped_column(Text)
    content_hash: Mapped[str] = mapped_column(String(64), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    repo: Mapped[Repo] = relationship(back_populates="units")
    file: Mapped[FileRecord] = relationship(back_populates="units")
    embeddings: Mapped[list[CodeUnitEmbedding]] = relationship(back_populates="unit", cascade="all, delete-orphan")
    __table_args__ = (UniqueConstraint("repo_id", "file_id", "qualname", "start_line", "end_line", name="uq_unit_identity"),)

class CodeUnitEmbedding(Base):
    __tablename__ = "code_unit_embeddings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    repo_id: Mapped[str] = mapped_column(ForeignKey("repos.id"), index=True)
    unit_id: Mapped[int] = mapped_column(ForeignKey("code_units.id"), index=True)
    model: Mapped[str] = mapped_column(String(255), index=True)
    dim: Mapped[int] = mapped_column(Integer)
    vector: Mapped[bytes] = mapped_column(LargeBinary)
    content_hash: Mapped[str] = mapped_column(String(64), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    unit: Mapped[CodeUnit] = relationship(back_populates="embeddings")
    __table_args__ = (UniqueConstraint("unit_id", "model", "content_hash", name="uq_unit_model_hash"),)
