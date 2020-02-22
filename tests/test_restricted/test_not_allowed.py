from likepy import  restrictedpy
from likepy.exceptions import CompileError
import pytest


restricted_eval = restrictedpy.exec
restricted_eval = restrictedpy.eval



def test_not_allowed_Ellipsis():
    """It prevents using the `ellipsis` statement."""
    with pytest.raises(CompileError, match=r".*Ellipsis statements are not allowed.*"):
        result = restricted_eval('...')
