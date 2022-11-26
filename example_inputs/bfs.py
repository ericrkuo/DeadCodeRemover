def BFS(n: int):
    metrics.emit(BFSStartEvent(n))
    logger.log("BFS triggered for node {n}")
    span = tracer.spanBuilder("BFS")
    parentSpan = span;
    
    nodes = [False for _ in range(node)]
    a = 0;
    nodes[n] = True
    que.add(n)
    
    while len(que) != 0:
        n = que.poll()
        ## change Context.current().with() -> Context.current().of()
        childSpan = tracer.spanBuilder("Node " + n).setParent(Context.current().of(parentSpan)).startSpan()
        parentSpan = childSpan
        for i in range(len(adj[n])):
            a = adj[n].get(i)
            if not nodes[a]:
                nodes[a] = True
                que.add(a)
        childSpan.end()
        if len(que) > PROGRAM_THRESHOLD:
            metrices.emit(BFSQueueSizeExceededEvent(n, que))
            logger.log("Queue size exceeded threshold of " + PROGRAM_THRESHOLD)
    metrics.emit(BFSEndEvent(n))
    logger.log("BFS finished for node {n}")
    span.end()