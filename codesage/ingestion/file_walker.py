from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os
from codesage.ingestion.language import detect_language

DEFAULT_EXCLUDE_DIRS = {".git", "node_modules", "dist", "build", ".venv", "venv", "__pycache__"}

@dataclass
class DiscoveredFile:
    path: Path
    rel_path: str
    language: str
    size_bytes: int
    mtime_epoch: int


def walk_repo(root: Path, exclude_dirs: set[str] | None = None, max_file_size_bytes: int = 2_000_000):
    exclude = DEFAULT_EXCLUDE_DIRS | (exclude_dirs or set())
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in exclude]
        for fn in filenames:
            p = Path(dirpath) / fn
            try:
                st = p.stat()
            except OSError:
                continue
            if st.st_size > max_file_size_bytes:
                continue
            rel = str(p.relative_to(root))
            lang = detect_language(p).language
            yield DiscoveredFile(path=p, rel_path=rel, language=lang, size_bytes=st.st_size, mtime_epoch=int(st.st_mtime))
