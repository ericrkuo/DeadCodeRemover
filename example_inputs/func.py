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

fn2()
x = fn(x, x)
