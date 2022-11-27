from jinja2 import Environment, FileSystemLoader
import os

class ReportGenerator:

    def generateHTMLReport(
        self,
        outputDir,
        input,
        output,
        linesRemovedArr,
        effectiveVariableMap, 
        linesDependentOnMap,
        ratioLinesRemoved,
        dependMap,
        effectiveVariables,
        fileName
    ):
        '''
        Generates an HTML report using Jinja
  
        Parameters:
        - outputDir - directory to generate HTML report
        - input - input source code
        - output - output score code (dead code removed)
        - linesRemovedArr - array of lines that were removed
        - effectiveVariableMap - map of each effective variable to its program slice
        - linesDependentOnMap - state.M
        - ratioLinesRemoved - number between 0 and 1 representing ratio of lines removed to total number of lines
        - dependMap -map of each line to its DependStat
        - effectiveVariables - list of effective variables
        - fileName - original file name where source code was read from
        '''
        root = os.path.dirname(outputDir)
        env = Environment( loader = FileSystemLoader("") )
        template = env.get_template('ui/template.html')  

        filename = os.path.join(root, 'output.html')
        with open(filename, 'w') as fh:
            fh.write(template.render(
                originalCode = input,
                deletedCode = output,
                linesRemoved = linesRemovedArr,
                numberOfLinesRemoved = len(linesRemovedArr),
                variableUsedIn = effectiveVariableMap,
                linesDependentOnMap = linesDependentOnMap,
                ratioLinesRemoved = ratioLinesRemoved,
                dependMap = dependMap,
                effectiveVariables = effectiveVariables,
                fileName = fileName
            ))

# public void BFS(int n)  
# {  
#     this.metrics.emit(new BFSStartEvent(n));
#     this.logger.log("BFS triggered for node {n}")
#     Span span = tracer.spanBuilder("BFS").startSpan();
#     Span parentSpan = span;
#     boolean nodes[] = new boolean[node];       
#     int a = 0;  
#     nodes[n]=true;                    
#     que.add(n);      
#     while (que.size() != 0)  
#     {  
#         n = que.poll();         
#         Span childSpan = tracer.spanBuilder("Node " + n)
#               .setParent(Context.current().with(parentSpan))
#               .startSpan();
#         parentSpan = childSpan; 
#         for (int i = 0; i < adj[n].size(); i++)  
#         {  
#             a = adj[n].get(i);  
#             if (!nodes[a])      
#             {  
#                 nodes[a] = true;  
#                 que.add(a);  
#             }  
#         } 
        
#         childSpan.end();
#         if (que.size() > this.PROGRAM_THRESHOLD) {
#             this.metrics.emit(new BFSQueueSizeExceededEvent(n, que));
#             this.logger.log("Queue size exceeded threshold of " + this.PROGRAM_THRESHOLD);
#         }
#     } 
#     this.metrics.emit(new BFSEndEvent(n));
#     this.logger.log("BFS finished for node {n}")
#     span.end();
# }  
# """


# deletedCode = """
# public void BFS(int n)  
# {  
#     boolean nodes[] = new boolean[node];       
#     int a = 0;  
#     nodes[n]=true;                    
#     que.add(n);      
#     while (que.size() != 0)  
#     {  
#         n = que.poll();         
#         for (int i = 0; i < adj[n].size(); i++)  
#         {  
#             a = adj[n].get(i);  
#             if (!nodes[a])      
#             {  
#                 nodes[a] = true;  
#                 que.add(a);  
#             }  
#         } 
#     }
# }   
# """

# linesRemoved = [3,4,5,6,14,15,16,17,27,28,29,30,31,32,33,34,35,36]
# effectiveVariables = {"nodes[]": [7,9,11,12,18,19,21,22,23,25,26,33],
#                         "a" : [8,11,12,18,19,20,21,22,23,24,25,26,33],
#                         "que" : [10,11,12,18,19,20,21,22,24,25,26,33]}
# htmlReport = ReportGenerator()
# htmlReport.generateHTMLReport(originalCode.strip(), deletedCode.strip(),linesRemoved, effectiveVariables)
