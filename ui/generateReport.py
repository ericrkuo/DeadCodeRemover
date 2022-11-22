from jinja2 import Environment, FileSystemLoader
import os

class ReportGenerator:

# input is the original code and output is code after deleting dead code
# lines removed is an list with the line number removed
    def generateHTMLReport(self, input, output, linesRemovedArr, effectiveVariableMap):
        root = os.path.dirname(os.path.abspath(__file__))
        env = Environment( loader = FileSystemLoader("") )
        template = env.get_template('ui/template.html')
        codeWithVariable = {}
        # converting line number to code for that line
        for key in effectiveVariableMap:
            temp = self.getCodeFromLine(input, effectiveVariableMap[key])
            codeWithVariable[key]= self.linesArrayToString(temp)      
        print(codeWithVariable)
        filename = os.path.join(root, 'output.html')
        with open(filename, 'w') as fh:
            fh.write(template.render(
                originalCode = input,
                deletedCode = output,
                linesRemoved = linesRemovedArr,
                numberOfLinesRemoved = len(linesRemoved),
                variableUsedIn = codeWithVariable
            ))

    def getCodeFromLine(self, input, lineNumbers):
        linesOfInput = input.splitlines()
        toRemove = []
        for i in range(0,len(linesOfInput)):
            if not (i+1 in lineNumbers):
                toRemove.append(linesOfInput[i])
        for rem in toRemove:
            linesOfInput.remove(rem)
        return linesOfInput
    # if we be nice if we could show the original line number, but that is hard todo, we can do that if we have extra time.
    def linesArrayToString(self, linesArray):
        codeBlock = ""
        for codeLine in linesArray:
            codeBlock += codeLine
            codeBlock += """
"""
        return codeBlock.strip()

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

linesRemoved = [3,4,5,6,14,15,16,17,27,28,29,30,31,32,33,34,35,36]
effectiveVariables = {"nodes[]": [7,9,11,12,18,19,21,22,23,25,26,33],
                        "a" : [8,11,12,18,19,20,21,22,23,24,25,26,33],
                        "que" : [10,11,12,18,19,20,21,22,24,25,26,33]}
htmlReport = ReportGenerator()
htmlReport.generateHTMLReport(originalCode.strip(), deletedCode.strip(),linesRemoved, effectiveVariables)
