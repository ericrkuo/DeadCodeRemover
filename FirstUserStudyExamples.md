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

> Note: is flow sensitive because depends on the return types of earlier statements

## 2. Function missing return type
```python
1 def foo(x):
2    if x > 0:
3        return x - 1
```

<details>
  <summary>Output (click me)</summary>
  
  ```
  Error: function foo is missing a return statement
  ```
</details>

> Note: is flow sensitive because depends on the structure of earlier statements 

## 3. Operations on variables of the wrong types
```python
1 if b:
2     x = 1
3 else: 
4    x = "foo"
5 print(x + 'hello') # this would generate a TypeError during runtime if b is True, but our project detects this statically
```

<details>
  <summary>Output (click me)</summary>
  
  ```
  Error: Operands for + operator has different types x (1) and y ('hello')
  ```
</details>

> Note: is flow sensitive because depends on data flow of variable types across branches

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

> Note: is flow sensitive because analyzing variables depends on whether they are defined as loop variables in earlier statements

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

> Note: is flow sensitive because analyzing closures depends on whether the variables were defined in a loop in earlier statements

## 6. Else clause on loop without a break statement
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

> Note: is flow sensitive because depends on whether the else block is defined for a `for` loop and whether the for loop has a break statement