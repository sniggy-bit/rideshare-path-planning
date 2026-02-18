#import deque from collections. Double-ended queues allow enqueuing and dequeuing in O(1) time.
from collections import deque
#import the grid class to access the get_neighbors function
from src.graph.grid import Grid

def bfs_shortest_path(grid:Grid, start, target,grid_array):
    #Data structure for path reconstruction
    path = []

    # Basic input validation
    if start is None or target is None:
        raise ValueError("`start` and `target` must be provided")

    #Initialize start and target nodes in grid array for visualization
    grid_array[start[0], start[1]] = 2 # Frontier
    grid_array[target[0], target[1]] = 2 # Frontier
    #Initialize a queue which will track visited nodes
    q = deque()
    #Store a set with valid BFS. This ensures checking with O(1) time complexity.
    visited = set()
    #The start node is a special case and doesn't have a predecessor, so we assign it a value of None in the hashmap.
    parent = {start:None}
    #Add the start node to the set and the queue
    visited.add(start)
    q.append(start)

    ##BFS Shortest Path Logic

    #The queue tracks nodes that need to be explored. Once a node has been visited, it is popped from the queue
    # and explored. Once all nodes are visited and explored, the queue becomes empty and the BFS is ended.
    while q:
        explore = q.popleft()
        
        # Color coding for visualization:
        # 3 = Visited/Exploring, 2 = Frontier (in queue)
        grid_array[explore[0], explore[1]] = 3 
        
        #Once a node has been popped from the queue, it will be explored.
        adj = grid.get_neighbors(explore)
        #For loop to explore the current node
        for i in adj:
            #Check whether i already exists in the BFS set. If not, add to set and the queue as the next node to visit.
            if i not in visited:
                visited.add(i)
                q.append(i)
                # Mark as Frontier
                grid_array[i[0], i[1]] = 2 

                #Add the node to the dictionary and track its parent
                parent[i] = explore
                
                if i == target:      
                #Path Reconstruction Code
                    #Create a path vector to store the path (in reverse, from target -> start)
                    current = target
                    while current is not None:
                        path.append(current)
                        # Color the final path a unique value (e.g., 5)
                        grid_array[current[0], current[1]] = 5
                        current = parent[current]
                    path.reverse()
                    
                    #Yield the final path and grid array for visualization
                    yield grid_array
                    return {"path" : path ,
                                "length" : len(path) - 1}
        #Yield the grid array for visualization after each node exploration
        yield grid_array  
    #If the target node doesn't exist, return None
    return None
