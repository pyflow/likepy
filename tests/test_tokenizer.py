
from likepy.tokenizer import LikepyTokenizer

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

def test_simple_token_1():
    t = LikepyTokenizer(code=code)
    for token in t.get_tokens():
        print(token)
    assert token.type == 0