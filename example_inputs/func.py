x = 2
y = 5

def fn(a, b):
    y = a
    a += 2
    z = y + a
    return z

x = fn(x, y)

def fn2(a, b):
    z = 5
    print(a)

fn2(1, fn2(x, y))
x = fn(fn2(x, 1), x)
