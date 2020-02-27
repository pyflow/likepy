
import parso
from likepy.compiler import dump_ast

code = '''
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
    module = parso.parse(code)
    dump_ast(module)