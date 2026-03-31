from __future__ import annotations
from typing import Dict
from codesage.parsing.base import BaseParser
from codesage.parsing.python_ast import PythonASTParser

_PARSERS: Dict[str, BaseParser] = {"python": PythonASTParser()}

def get_parser(language: str) -> BaseParser | None:
    return _PARSERS.get(language)
