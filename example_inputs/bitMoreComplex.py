min, max = 0,0
sum, avg = 0,0
A,B,C = 0,0,0
i,f = 0,0
i=5
m=i
f=m
print("Enter three numbers")
A = int(input('Enter 1st number: '))
B = int(input('Enter 2nd number: '))
C = int(input('Enter 3rd number: '))

for s in range(5):
  m = m + 2
  if f == 1:
    print("A>1")
  if f == 2:
    print(f"A={A}")
  if f == 3:
    sum = 0
  
  if A > B and A > C:
    max = A
  if B > A and B > C:
    max = B
  if C > A and C > B:
    max = C
  print(f"Max={max}")
  
  if A < B and A < C:
    min = A
  if B < A and B < C:
    min = B
  if C < A and C < B:
    min = C
  print(f"Min={min}")

  if m == 10:
    m = m + 5
  elif m == 20:
    m=0
  elif m==30:
    m=10
  
  sum = A + B + C
  avg = sum/3
  print(f'sum={sum}')
  print(f'avg={avg}')
