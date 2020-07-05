from contextlib import contextmanager


@contextmanager
def mock_input(return_value):
    original_input_func = __builtins__["input"]
    __builtins__["input"] = lambda _: return_value
    yield
    __builtins__["input"] = original_input_func
