# Examples for First User Study

## 1. Returning different types in a function
```python
1 def my_function(name):
2    if name == 'CPSC 410':
3        return 'Group 12'
4    else:
5        return 1
```

<details>
  <summary>Output (click me)</summary>
  
  ```
  Error: my_function has different return types on line 3 and 5
  ```
</details>

## 2. Function missing return type
```python
1 def foo(x: int) -> int:
2    if x > 0:
3        return x - 1
```

<details>
  <summary>Output (click me)</summary>
  
  ```
  Error: function foo should is missing a return statement
  ```
</details>

## 3. Operations on variables of the wrong types
```python
1 x = 1
2 y = 'hello'
3 print(x+y) # this would generate a TypeError, but our project detects this statically  
```

<details>
  <summary>Output (click me)</summary>
  
  ```
  Error: Operands for + operator has different types x (1) and y ('hello')
  ```
</details>

## 4. Redefined Loop Variables
```python
1 for i in range(4):
2    print(i)
3    i = 10
```

<details>
  <summary>Output (click me)</summary>
  
  ```
  Error: Loop variable i overwritten in body on line 3
  ```
</details>

## 5. Cell variable defined in loop

```python
1 def foo(numbers):
2    for i in numbers:
3        def bar():
4            print(i)
5        bar()
```

<details>
  <summary>Output (click me)</summary>
  
  ```
  Error: Cell variable i used in closure for function bar is defined in a loop
  ```
</details>

### Else clause on loop without a break statement
```python
1 def contains(list, number):
2    for i in list:
3        if i == number:
4            print("List contains number")
5    else:
6        print("List does not contain number")
```

<details>
  <summary>Output (click me)</summary>
  
  ```
  Error: potential unintended behavior detected in for loop with else clause on line 6 since no break statement
  ```
</details>
