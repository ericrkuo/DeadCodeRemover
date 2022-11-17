x = 42
y = x

# multiple declarations in one line
s, b = y, 100

# declaring an array
a = [x, y]

# assign same value to multiple variables
e = r = a

# assign same value to multiple tuples
# in this case, (a,b) and (c,d) do not depend on each other, they depend on (x,y)
(a,b) = (c,d) = (x+y,y)

# basic assignments
z = 4
w = 14
w = x + y + z
z = w
z = y - z
print(x)
print(y)
print(z)
print(w)