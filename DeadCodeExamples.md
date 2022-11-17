# Practical Examples of Dead Code

## Code instrumentation that obstructs the core logic of a program

In real world scenarios, code is often instrumented with things like logging, metrics, and tracing. However, these can cloud away the core logic of the program, and is considered dead code since it doesn't yielf results to the core logic of the program.

For example, consider this pseudocode implementing breadth first search. After a bunch of the dead code is removed, the resulting program is on the right. It's much easier to understand, not only for the original developer who wrote the code, but also for new developers who may be new to the code base and tasked with modifying the code.

<table>
<tr>
<th>Program with dead code</th>
<th>Program after removing dead code</th>
</tr>
<tr>
<td>
  
```java
public void BFS(int n)  
{  
    this.metrics.emit(new BFSStartEvent(n));
    this.logger.log("BFS triggered for node {n}")
    Span span = tracer.spanBuilder("BFS").startSpan();
    Span parentSpan = span;
    boolean nodes[] = new boolean[node];         
    int a = 0;  
    nodes[n]=true;                    
    que.add(n);        
    while (que.size() != 0)  
    {  
        n = que.poll();         
        Span childSpan = tracer.spanBuilder("Node " + n)
              .setParent(Context.current().with(parentSpan))
              .startSpan();
        parentSpan = childSpan; 
        for (int i = 0; i < adj[n].size(); i++)  
        {  
            a = adj[n].get(i);  
            if (!nodes[a])       
            {  
                nodes[a] = true;  
                que.add(a);  
            }  
        } 
        
        childSpan.end();
        if (que.size() > this.PROGRAM_THRESHOLD) {
            this.metrics.emit(new BFSQueueSizeExceededEvent(n, que));
            this.logger.log("Queue size exceeded threshold of " + this.PROGRAM_THRESHOLD);
        }
    }  
    this.logger.log("BFS finished for node {n}")
    span.end();
}  
```
  
</td>
<td>

```java
void BFS(int n)  
{  
    boolean nodes[] = new boolean[node];       
    int a = 0;  
    nodes[n]=true;                    
    que.add(n);       
    while (que.size() != 0)  
    {  
        n = que.poll();        
        System.out.print(n+" ");      
        for (int i = 0; i < adj[n].size(); i++)    
        {  
            a = adj[n].get(i);  
            if (!nodes[a])      
            {  
                nodes[a] = true;  
                que.add(a);  
            }  
        }    
    }  
}  
```

</td>
</tr>
</table>
