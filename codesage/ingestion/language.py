from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

EXT_TO_LANG = {".py": "python"}

@dataclass(frozen=True)
class LanguageInfo:
    language: str
    reason: str


def detect_language(path: str | Path) -> LanguageInfo:
    p = Path(path)
    ext = p.suffix.lower()
    if ext in EXT_TO_LANG:
        return LanguageInfo(EXT_TO_LANG[ext], f"extension:{ext}")
    return LanguageInfo("unknown", "extension:unknown")
