x = 2
y = 5

def fn(a, b):
    y = a
    a += 2
    z = y + a
    return z


x = fn(x, y)
