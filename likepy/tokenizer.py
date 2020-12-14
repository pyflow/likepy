
import tokenize
from io import BytesIO

class LikepyTokenizer:
    def __init__(self, sourcepath=None, code=None):
        self.sourcepath=sourcepath
        self.code = code

    def get_tokens(self):
        if not self.sourcepath and not self.code:
            raise Exception('Either sourcepath or code must be set.')
        if self.sourcepath:
            with open(self.sourcepath, 'rb') as sf:
                return tokenize.tokenize(sf.readline)
        else:
            return tokenize.tokenize(BytesIO(self.code.encode('utf-8')).readline)