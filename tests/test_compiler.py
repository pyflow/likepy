
from likepy.compiler import LikepyCompiler
from likepy.asthelper import dump_code

lkpy = LikepyCompiler()

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
    module = lkpy.compile(code)