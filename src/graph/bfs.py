#import deque from collections. Double-ended queues allow enqueuing and dequeuing in O(1) time.
from collections import deque

def bfs(start, target, grid):

    #Helper function to get neighbors of a node in the grid
    def get_neighbors(node):
        #implement getting neighbors from the grid
        neighbors = []
        return neighbors
    
    # Basic input validation
    if start is None or target is None:
        raise ValueError("`start` and `target` must be provided")

    #Initialize a queue which will track visited nodes
    q = deque()
    #Store a set with valid BFS. This ensures checking with O(1) time complexity.
    visited = set()
    #The start node is a special case and doesn't have a predecessor, so we assign it a value of None in the hashmap.
    parent = {start:None}
    #Add the start node to the set and the queue
    visited.add(start)
    q.append(start)

    # TODO: implement BFS loop here
    #The queue tracks nodes that need to be explored. Once a node has been visited, it is popped from the queue
    # and explored. Once all nodes are visited and explored, the queue becomes empty and the BFS is ended.
    while q:
        explore = q.popleft()
        
        #Once a node has been popped from the queue, it will be explored.
        adj = get_neighbors(explore)
        #For loop to explore the current node
        for i in adj:
            #Check whether i already exists in the BFS set. If not, add to set and the queue as the next node to visit.
            if i not in visited:
                visited.add(i)
                q.append(i)
                #Add the node to the dictionary and track its parent
                parent[i] = explore
                if i == target:
                        
                #Path Reconstruction Code
                    #Create a path vector to store the path (in reverse, from target -> start)
                    path = []
                    path.append(target)
                    j = 0
                    while parent[path[j]] is not None:
                        path.append(parent[path[j]])
                        j = j + 1
                    path.reverse()
                    return {"path" : path ,
                                "length" : len(path) - 1}
    #If the target node doesn't exist, return None
    return None

#Test the code above and print a valid BFS which ends at the target
graph = [[0,1],[0,2],[0,3],[1,2],[2,3],[2,4],[3,4],[4,5],[4,6]]
bfs(graph,5,6)
