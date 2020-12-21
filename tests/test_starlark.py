from likepy.starlark import StarLarkParser
from likepy.asthelper import dump_tree
import ast

code = '''
def controlflow():
    pass
'''

def test_simple_parse_1():
    p = StarLarkParser(code=code)
    m = p.parse()
    print(m)
    print(dump_tree(m))
    print(dump_tree(ast.parse(code)))