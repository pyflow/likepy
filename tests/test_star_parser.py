
import os
import fnmatch
import parso
from likepy.compiler import dump_ast, LikepyCompiler

lkpy = LikepyCompiler()

def test_star_parse():
    asset_dir = './assets/starlark'
    asset_files = os.listdir(asset_dir)
    pattern = "*.star"
    star_files = []
    for entry in asset_files:
        if fnmatch.fnmatch(entry, pattern):
            star_files.append(os.path.abspath(os.path.join(asset_dir, entry)))

    for star in star_files:
        with open(star, 'rb') as f:
            codes = f.read()
            for code in codes.decode('utf-8').split('---'):
                module = lkpy.compile(code)
                dump_ast(module)
                if star == 'assign.star':
                    break