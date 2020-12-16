
import os
import contextlib
import sys
import ast
from .starlark import StarLark, StarLarkParser

class LikepyCompiler:
    def __init__(self):
        pass

    def compile_file(self, file_path):
        with open(file_path, "rb") as f:
            code = f.read()
            file_name = os.path.basename(file_path)
            ext = os.path.extname(file_path)
            dialect = 'starlette' if ext == '.star' else ext[1:]
            return self.compile(code, file_name=file_name, dialect=dialect)

    def compile(self, source, file_name="<string>", dialect="starlette"):
        if dialect == 'starlette':
            starlark = StarLarkParser(code = source)
            starlark.parse()
        else:
            raise Exception('only support starlette dialect now.')
