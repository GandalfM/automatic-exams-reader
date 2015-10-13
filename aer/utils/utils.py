from functools import partial, reduce

combine = lambda *xs: partial(reduce, lambda v, x: x(v), xs)
