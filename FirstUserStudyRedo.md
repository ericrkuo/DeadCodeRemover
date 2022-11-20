# Examples for First User Study

## 1. Lines that doesn't change value of desired variable;

Desired variable: y

<table>
<tr>
<th>Program with dead code</th>
<th>Program after removing dead code</th>
</tr>
<tr>
<td>


```python
1 def my_fuction():
2   x=3
3   y=0
4   for i in range (0,5):
5       x= i
6       y += x
7       print(y)
8   return y
```


</td>
<td>


```python
1 def my_fuction():
2   x=3
3   y=0
4   for i in range (0,5):
5       x= i
6       y += x
8   return y
```

</td>
</tr>
</table>


<details>
  <summary>Output (click me)</summary>

  ```
  Lines removed: 7
  ```
</details>

> Note: print statement does not affect the value of y



## 2. Lines that doesn't change value of desired variable (cont.);
Desired variable: y
<table>
<tr>
<th>Program with dead code</th>
<th>Program after removing dead code</th>
</tr>
<tr>
<td>


```python
1 def my_function(name):
2   x=3
3   y=0
4   for i in range (0,5):
5       y += i
6       x= y
7       print(y)
8   return y
```


</td>
<td>


```python
1 def my_function(name):
3   y=0
4   for i in range (0,5):
5       y += i
8   return y
```

</td>
</tr>
</table>


<details>
  <summary>Output (click me)</summary>

  ```
  Lines removed: 2,6,7
  ```
</details>

> Note: since x is not the desired variable, and it doesn't affect y, it is 'dead code'

## 3. investigating certain non-returning variable 
Desired variable: numberOfNonInt
<table>
<tr>
<th>Program with dead code</th>
<th>Program after removing dead code</th>
</tr>
<tr>
<td>


```python
1 def roundFloatArray(array):
2     isWholeNumber = [False] * len(array);
3     wholeNumberArray = [0]*len(array)
4     numberOfNonInt = 0
5     for i in range (0,len(array)):
6         if(array[i] % 1 ==0):
7             isWholeNumber[i] = True
8             wholeNumberArray[i] = array[i]
9         else:
10             isWholeNumber[i] = False
11             wholeNumberArray[i] = round(array[i])
12             numberOfNonInt += 1;
13     print("numberOfNonInt:" , numberOfNonInt)
14     for i in range (0,len(isWholeNumber)):
15         if(isWholeNumber[i] == False):
16             print("number at index", i, "is not a whole number")
17     return wholeNumberArray
```


</td>
<td>


```python
1 def roundFloatArray(array):
4     numberOfNonInt = 0
5     for i in range (0,len(array)):
6         if(array[i] % 1 ==0):
9         else:
12            numberOfNonInt += 1;
```

</td>
</tr>
</table>

<details>
  <summary>Output (click me)</summary>

  ```
  Lines removed:2,3,7,8,10,11,13,14,15,16,17
  ```
</details>

> Note: all lines that does not affect the value of desired varaible are removed

## 4. Investigating returning variable
Desired variable: wholeNumberArray
<table>
<tr>
<th>Program with dead code</th>
<th>Program after removing dead code</th>
</tr>
<tr>
<td>


```python
1 def roundFloatArray(array):
2     isWholeNumber = [False] * len(array);
3     wholeNumberArray = [0]*len(array)
4     numberOfNonInt = 0
5     for i in range (0,len(array)):
6         if(array[i] % 1 ==0):
7             isWholeNumber[i] = True
8             wholeNumberArray[i] = array[i]
9         else:
10             isWholeNumber[i] = False
11             wholeNumberArray[i] = round(array[i])
12             numberOfNonInt += 1;
13     print("numberOfNonInt:" , numberOfNonInt)
14     for i in range (0,len(isWholeNumber)):
15         if(isWholeNumber[i] == False):
16             print("number at index", i, "is not a whole number")
17     return wholeNumberArray
```


</td>
<td>


```python
1 def roundFloatArray(array):
3     wholeNumberArray = [0]*len(array)
5     for i in range (0,len(array)):
6         if(array[i] % 1 ==0):
8             wholeNumberArray[i] = array[i]
9         else:
11             wholeNumberArray[i] = round(array[i])
17     return wholeNumberArray
```

</td>
</tr>
</table>

<details>
  <summary>Output (click me)</summary>

  ```
  Lines removed: 2,4,7,10,12,13,14,15,16
  ```
</details>

> Note: the core program is highlighted when we look investigate only returning variable

