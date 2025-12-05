def bfs(graph, node):
    visited = []      # list of nodes we’ve already seen
    queue = []        # list used as a queue (FIFO)

    visited.append(node)   # mark the starting node as visited
    queue.append(node)     # and put it in the queue

    while queue:           # run while there is something in the queue
        s = queue.pop(0)   # pop from the *front* of the queue
        print(s, end=" ")  # "visit" the node (here: just print it)

        # look at all neighbors of s
        for n in graph[s]:
            if n not in visited:   # if we haven't seen this neighbor yet
                visited.append(n)  # mark as visited
                queue.append(n)    # and add it to the queue


graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E', 'F'],
    'C': ['G'],
    'D': [],
    'E': [],
    'F': ['H'],
    'G': ['I'],
    'H': [],
    'I': [],
}

bfs(graph, 'A')