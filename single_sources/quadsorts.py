#!/usr/bin/env python3

"""
The idea is that if you compare numbers in a N^2 nested for loop and swap them, in many cases they seem to be sorted.

Probably "inspired" by https://arxiv.org/abs/2110.01111 (Is this the simplest (and most surprising) sorting algorithm ever? - Stanley P. Y. Fung)

"""

import itertools

def quadsort(a, i_range, j_range, idx1, idx2):
    # print("sorting with params", i_range, j_range, idx1, idx2)
    n = len(a)
    for i in i_range(N=n):
        # print(f"j_range({i})", j_range(i))
        for j in j_range(i, N=n):
            x1, x2 = idx1(i, j, N=n), idx2(i, j, N=n)
            # print("i", i, "j", j, "x1", x1, "x2", x2)
            if a[x1] < a[x2]:
                t = a[x1]
                a[x1] = a[x2]
                a[x2] = t

sorted_sample = [1, 1, 2, 2, 3, 3, 4, 4]

def quadsort_all(i_range, j_range, idx1, idx2):
    for perm in itertools.permutations(sorted_sample):
        perm = list(perm)
        # print("from", perm)
        try:
            quadsort(perm, i_range, j_range, idx1, idx2)
        except IndexError:
            # print("Index error with params", i_range, j_range, idx1, idx2)
            return False
        # print(" to ", perm)
        if sorted_sample != perm:
            return False

    return True


def try_all_quadsorts():
    sorted_sample = [1, 1, 2, 2, 3, 3, 4, 4]
    N = len(sorted_sample)

    # # Standard bubble sort
    # quadsort_all(lambda: range(0, N), lambda i: range(i, 0, -1), lambda i, j: (j, j-1))

    SYMBOL_I = -99990
    SYMBOL_J = -99991
    SYMBOL_N = -99992

    class _plus:
        def __str__(self):
            return '+'
        def __repr__(self):
            return '+'
        def __call__(self, a, b):
            return a + b

    class _minus:
        def __str__(self):
            return '-'
        def __repr__(self):
            return '-'
        def __call__(self, a, b):
            return a - b

    plus = _plus()
    minus = _minus()

    class custom_expr:
        def __init__(self, a, op, b):
            self.a = a
            self.b = b
            self.op = op

        def __str__(self):
            return f'expr("{self.a}{str(self.op)}{self.b}")'.replace(str(SYMBOL_J), "j").replace(str(SYMBOL_I), "i").replace(str(SYMBOL_N), "N")

        def __repr__(self):
            return self.__str__()

        def __call__(self, i=None, j=None, N=None):
            a = self.a
            b = self.b

            if a == SYMBOL_I:
                a = i
            if a == SYMBOL_J:
                a = j
            if a == SYMBOL_N:
                a = N

            if b == SYMBOL_I:
                b = i
            if b == SYMBOL_J:
                b = j
            if b == SYMBOL_N:
                b = N

            return self.op(a, b)

    class const_expr:
        def __init__(self, v):
            self.v = v

        def __call__(self, i=None, j=None, N=None):
            v = self.v
            if v == SYMBOL_I:
                v = i
            if v == SYMBOL_J:
                v = j
            if v == SYMBOL_N:
                v = N
            return v

        def __str__(self):
            return f'const({self.v})'.replace(str(SYMBOL_J), "j").replace(str(SYMBOL_I), "i").replace(str(SYMBOL_N), "N")

        def __repr__(self):
            return self.__str__()


    def expr(a, op=None, b=None):
        if op is None:
            return const_expr(a)
        return custom_expr(a, op, b)

    class custom_range:
        def __init__(self, start, stop, step):
            self.start = start
            self.stop = stop
            self.step = step

        def __str__(self):
            return f'{self.__class__.__name__}({self.start},{self.stop},{self.step})'

        def __repr__(self):
            return self.__str__()

    class i_range(custom_range):
        def __call__(self, i=None, j=None, N=None):
            return range(self.start(i, j, N), self.stop(i, j, N), self.step(i, j, N))

    class j_range(custom_range):
        def __call__(self, i, j=None, N=None):
            return range(self.start(i, j, N), self.stop(i, j, N), self.step(i, j, N))


    # TODO: for every plus or minus one, we should add another of the opposite. including 1  and -1

    i_ranges = []
    for i_start in (expr(0), expr(1), expr(SYMBOL_N, minus, 1), expr(SYMBOL_N)):
        for i_end in (expr(0), expr(1), expr(SYMBOL_N, minus, 1), expr(SYMBOL_N)):
            for i_step in (expr(1), expr(-1)):
                i_ranges.append(i_range(i_start, i_end, i_step))

    j_ranges = []
    for j_start in (expr(0), expr(1), expr(SYMBOL_N, minus, 1), expr(SYMBOL_N), expr(SYMBOL_I), expr(SYMBOL_I, minus, 1)):
        for j_end in (expr(0), expr(1), expr(SYMBOL_N, minus, 1), expr(SYMBOL_N), expr(SYMBOL_I), expr(SYMBOL_I, minus, 1)):
            for j_step in (expr(1), expr(-1)):
                j_ranges.append(j_range(j_start, j_end, j_step))

    indexers = [
        expr(0),
        expr(SYMBOL_N),
        expr(SYMBOL_I),
        expr(SYMBOL_J),
        expr(0 + 1),
        expr(SYMBOL_N, plus, 1),
        expr(SYMBOL_I, plus, 1),
        expr(SYMBOL_J, plus, 1),
        expr(0 - 1),
        expr(SYMBOL_N, minus, 1),
        expr(SYMBOL_I, minus, 1),
        expr(SYMBOL_J, minus, 1),
    ]

    # # Standard bubble sort
    # quadsort_all(lambda: range(0, N), lambda i: range(i, 0, -1), lambda i, j: (j, j-1))

    # i_ranges = (i_range(expr(0), expr(N), expr(1)), )
    # j_ranges = (j_range(expr(SYMBOL_I), expr(0), expr(-1)), )
    # indexers = (expr(SYMBOL_J), expr(SYMBOL_J, minus, 1))

    for i_range in i_ranges:
     for j_range in j_ranges:
      for indexer1 in indexers:
       for indexer2 in indexers:
        # print(i_range, j_range, indexer1, indexer2)
        result = quadsort_all(i_range, j_range, indexer1, indexer2)
        if result:
            print("GOOD", i_range, j_range, indexer1, indexer2)





try_all_quadsorts()
