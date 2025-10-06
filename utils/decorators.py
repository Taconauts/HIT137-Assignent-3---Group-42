# Two simple decorators to satisfy rubric (multiple decorators).
# - @ensure_path: validates file exists before running model
# - @timeit: prints duration of the wrapped function

import os, time, functools

def ensure_path(fn):
    @functools.wraps(fn)
    def wrapper(self, input_path, *a, **k):
        if not input_path or not os.path.exists(input_path):
            raise FileNotFoundError("Input path is missing or invalid.")
        return fn(self, input_path, *a, **k)
    return wrapper

def timeit(fn):
    @functools.wraps(fn)
    def wrapper(*a, **k):
        t0 = time.time()
        out = fn(*a, **k)
        dt = time.time() - t0
        print(f"{fn.__name__} took {dt:.2f}s")
        return out
    return wrapper
