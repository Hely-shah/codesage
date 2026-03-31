from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

@dataclass
class ParsedUnit:
    unit_type: str
    name: str
    qualname: str
    signature: str | None
    start_line: int
    end_line: int
    docstring: str | None
    code: str

class BaseParser:
    language: str
    def parse(self, text: str, file_path: str) -> Iterable[ParsedUnit]:
        raise NotImplementedError
