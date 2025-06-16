#!/usr/bin/env python

def eval_3nCn_div_2nCn_sqrtn(n):
    x = []
    k = 1
    for i in range(0, n):
        k = k * (3 * n - i) / (2 * n - i)
        if i % 100 == 9:
            x.append(eval_root_n(k, n))
            k = 1
    
    x.append(eval_root_n(k, n))
    k = 1
    for v in x:
        k = k * v

    return k

def eval_root_n(x, n):
    return x ** (1/n)

N = 9999999

print(eval_3nCn_div_2nCn_sqrtn(N))
