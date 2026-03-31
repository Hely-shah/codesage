from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import hashlib
import logging
from git import Repo as GitRepo

logger = logging.getLogger(__name__)

@dataclass
class CloneResult:
    repo_id: str
    local_path: Path
    default_branch: str | None
    head_commit: str | None


def stable_repo_id(repo_url: str) -> str:
    return hashlib.sha1(repo_url.encode("utf-8")).hexdigest()


def clone_or_update(repo_url: str, dest_root: Path) -> CloneResult:
    dest_root.mkdir(parents=True, exist_ok=True)
    repo_id = stable_repo_id(repo_url)
    dest = dest_root / repo_id
    if dest.exists() and (dest / ".git").exists():
        gr = GitRepo(str(dest))
        gr.remotes.origin.fetch(prune=True)
        try:
            gr.git.pull("--ff-only")
        except Exception:
            logger.warning("Pull failed; continuing")
    else:
        gr = GitRepo.clone_from(repo_url, str(dest))

    try:
        default_branch = gr.active_branch.name
    except Exception:
        default_branch = None

    try:
        head_commit = gr.head.commit.hexsha
    except Exception:
        head_commit = None

    return CloneResult(repo_id=repo_id, local_path=dest, default_branch=default_branch, head_commit=head_commit)
