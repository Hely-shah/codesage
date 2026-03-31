from __future__ import annotations
from codesage.db.models import CodeUnit

def build_representation(unit: CodeUnit, file_path: str | None = None) -> str:
    parts: list[str] = []
    parts.append(f"TYPE: {unit.unit_type}")
    parts.append(f"QUALNAME: {unit.qualname}")
    if unit.signature:
        parts.append(f"SIGNATURE: {unit.signature}")
    if file_path:
        parts.append(f"FILE: {file_path}")
    if unit.docstring:
        parts.append("DOCSTRING:\n" + unit.docstring)
    parts.append("CODE:\n" + unit.code)
    return "\n".join(parts)

