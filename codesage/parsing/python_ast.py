from __future__ import annotations
import ast
import logging
from typing import Iterable
from codesage.parsing.base import BaseParser, ParsedUnit

logger = logging.getLogger(__name__)

def _get_source_segment(lines: list[str], start_line: int, end_line: int) -> str:
    return "".join(lines[start_line-1:end_line])

def _format_args(args: ast.arguments) -> str:
    parts: list[str] = []
    def add(a):
        if a is None:
            return
        if hasattr(a, "arg"):
            parts.append(a.arg)
    for a in getattr(args, "posonlyargs", []):
        add(a)
    if getattr(args, "posonlyargs", []):
        parts.append("/")
    for a in args.args:
        add(a)
    if args.vararg:
        parts.append("*" + args.vararg.arg)
    elif args.kwonlyargs:
        parts.append("*")
    for a in args.kwonlyargs:
        add(a)
    if args.kwarg:
        parts.append("**" + args.kwarg.arg)
    return "(" + ", ".join(parts) + ")"

def _end_lineno(node: ast.AST) -> int:
    end = getattr(node, "end_lineno", None)
    if isinstance(end, int):
        return end
    max_line = getattr(node, "lineno", 1)
    for child in ast.walk(node):
        ln = getattr(child, "end_lineno", None) or getattr(child, "lineno", None)
        if isinstance(ln, int):
            max_line = max(max_line, ln)
    return max_line

class PythonASTParser(BaseParser):
    language = "python"
    def parse(self, text: str, file_path: str) -> Iterable[ParsedUnit]:
        try:
            tree = ast.parse(text)
        except SyntaxError as e:
            logger.warning("SyntaxError in %s: %s", file_path, e)
            return []
        lines = text.splitlines(keepends=True)
        units: list[ParsedUnit] = []
        mod_doc = ast.get_docstring(tree)
        if mod_doc:
            end = 1
            for n in tree.body:
                if isinstance(n, ast.Expr) and isinstance(getattr(n, "value", None), (ast.Str, ast.Constant)):
                    end = _end_lineno(n)
                    break
            units.append(ParsedUnit("module","__module__","__module__",None,1,end,mod_doc,_get_source_segment(lines,1,end)))

        class Stack:
            def __init__(self): self.names=[]
            def push(self,n): self.names.append(n)
            def pop(self): self.names.pop()
            def qual(self,n): return ".".join(self.names+[n]) if self.names else n
        stack=Stack()

        def visit(node):
            for child in ast.iter_child_nodes(node):
                if isinstance(child,(ast.FunctionDef, ast.AsyncFunctionDef)):
                    qn=stack.qual(child.name)
                    sig=child.name+_format_args(child.args)
                    start=getattr(child,"lineno",1)
                    end=_end_lineno(child)
                    units.append(ParsedUnit("function",child.name,qn,sig,start,end,ast.get_docstring(child),_get_source_segment(lines,start,end)))
                    stack.push(child.name); visit(child); stack.pop()
                elif isinstance(child, ast.ClassDef):
                    qn=stack.qual(child.name)
                    start=getattr(child,"lineno",1)
                    end=_end_lineno(child)
                    units.append(ParsedUnit("class",child.name,qn,f"class {child.name}",start,end,ast.get_docstring(child),_get_source_segment(lines,start,end)))
                    stack.push(child.name); visit(child); stack.pop()
                else:
                    visit(child)
        visit(tree)
        return units
