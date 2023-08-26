def test(a, b, c=123, d=321):
    return a, b, c, d


print(test(1, 2, d=33))
