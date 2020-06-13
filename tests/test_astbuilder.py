
import parso
from likepy.compiler import dump_ast
from likepy.starlark import StarlarkGrammar
from likepy.astbuilder import ASTBuilder
import ast
from likepy.asthelper import dump_code

code = '''
("Hello")
True
False
None
load("assert.star", "assert")

def controlflow():
    # elif
    x = 0
    if True:
        x=1
    elif False:
        assert.fail("else of true")
    else:
        assert.fail("else of else of true")
    assert.true(x)
'''

def test_dump():
    grammar = StarlarkGrammar()
    module = grammar.parse(code)
    dump_code(code.replace('assert', 'massert'))
    dump_ast(module)
    b = ASTBuilder(module)
    b.build_ast()