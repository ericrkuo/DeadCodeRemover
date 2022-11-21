from jinja2 import Environment, FileSystemLoader
import os

class generateReport:
    def __init__(self, input, output):
        self.input = input
        self.output = output


    def generateHTMLReport(self):
        root = os.path.dirname(os.path.abspath(__file__))
        env = Environment( loader = FileSystemLoader("") )
        template = env.get_template('template.html')
        
        
        filename = os.path.join(root, 'output.html')
        with open(filename, 'w') as fh:
            fh.write(template.render(
                originalCode = self.input,
                deletedCode = self.output
            ))


originalCode = """
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
    this.metrics.emit(new BFSEndEvent(n));
    this.logger.log("BFS finished for node {n}")
    span.end();
}  
"""


deletedCode = """
public void BFS(int n)  
{  
    boolean nodes[] = new boolean[node];       
    int a = 0;  
    nodes[n]=true;                    
    que.add(n);      
    while (que.size() != 0)  
    {  
        n = que.poll();         
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
"""

htmlReport = generateReport(originalCode.rstrip(), deletedCode.rstrip())




htmlReport.generateHTMLReport()
