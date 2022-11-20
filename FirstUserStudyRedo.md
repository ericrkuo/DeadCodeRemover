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

## 4. Code instrumentation that obstructs the core logic of a program

In real world scenarios, code is often instrumented with things like logging, metrics, and tracing. However, these can cloud away the core logic of the program, and is considered dead code since it doesn't yield results to the main functionality of the program.

For example, consider this pseudocode implementing breadth first search. After a bunch of the dead code is removed, the resulting program is on the right. It's much easier to understand, not only for the original developer who wrote the code, but also for new developers who may be new to the code base and tasked with modifying the code.

Desired variable: `que` and `nodes`

<table>
<tr>
<th>Program with dead code</th>
<th>Program after removing dead code</th>
</tr>
<tr>
<td>
  
```python
1 public void BFS(int n)  
2 {  
3    this.metrics.emit(new BFSStartEvent(n));
4    this.logger.log("BFS triggered for node {n}")
5    Span span = tracer.spanBuilder("BFS").startSpan();
6    Span parentSpan = span;
7    boolean nodes[] = new boolean[node];         
8    int a = 0;  
9    nodes[n]=true;                    
10    que.add(n);        
11    while (que.size() != 0)  
12    {  
13      n = que.poll();         
14      Span childSpan = tracer.spanBuilder("Node " + n)
15            .setParent(Context.current().with(parentSpan))
16            .startSpan();
17      parentSpan = childSpan; 
18      for (int i = 0; i < adj[n].size(); i++)  
19      {  
20         a = adj[n].get(i);  
21          if (!nodes[a])       
22         {  
23              nodes[a] = true;  
24              que.add(a);  
25          }  
26      } 
27      
28      childSpan.end();
29      if (que.size() > this.PROGRAM_THRESHOLD) {
30          this.metrics.emit(new BFSQueueSizeExceededEvent(n, que));
31          this.logger.log("Queue size exceeded threshold of " + this.PROGRAM_THRESHOLD);
32      }
33   } 
34  this.metrics.emit(new BFSEndEvent(n));
35  this.logger.log("BFS finished for node {n}")
36  span.end();
37 }  
```
  
</td>
<td>

```python
1 public void BFS(int n)  
2 {  
3    boolean nodes[] = new boolean[node];       
4    int a = 0;  
5    nodes[n]=true;                    
6    que.add(n);       
7    while (que.size() != 0)  
8    {  
9        n = que.poll();        
10        System.out.print(n+" ");      
11        for (int i = 0; i < adj[n].size(); i++)    
12        {  
13            a = adj[n].get(i);  
14            if (!nodes[a])      
15            {  
16                nodes[a] = true;  
17                que.add(a);  
18            }  
19        }    
20    }  
21 }  
```

</td>
</tr>
</table>

<details>
  <summary>Output (click me)</summary>

  ```
  Lines removed: 3,4,5,6,14,15,16,17,28,29,30,31,32,34,35,36
  ```
</details>
