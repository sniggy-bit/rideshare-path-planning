#Module containing functions to evaluate the cost and quality of a route

#Imports
import numpy as np
from src.graph.bfs import bfs_shortest_path
from src.graph.grid import Grid

#Path cost finder function: given a grid, a valid route and a bfs_shortest_path function, 
# returns the total cost of the path that goes through all the stops in the order they are given
def path_cost_finder(grid, route, bfs_shortest_path):
    total_cost = 0
    for i in range(len(route)-1):
        start = route[i][2]
        end = route[i+1][2]
        #find shortest path between two adjacent stops using bfs_shortest_path function
        path = bfs_shortest_path(grid, start, end)
        print(f"Path from {start} to {end}: {path}")
        if path["length"] is None:
            return None #If there is no path between two stops, return infinity
        total_cost += path["length"] #The cost of the path is the number of edges, which is the number of nodes - 1
    return total_cost
