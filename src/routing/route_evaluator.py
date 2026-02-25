#Module containing functions to evaluate the cost and quality of a route

#Imports
import numpy as np
from src.graph.path_finder import bfs_shortest_path
from src.graph.grid import Grid

#Manhattan distance function: given two locations (x1, y1) and (x2, y2), returns the manhattan distance between them
def get_dist(loc1, loc2):
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])



#Path cost finder function T(r): given a grid, a valid route and a bfs_shortest_path function, 
# returns the total cost of the path that goes through all the stops in the order they are given
def path_cost_finder(grid,route, bfs_shortest_path,cache,mode = "simple"):
    total_cost = 0
    for i in range(len(route)-1):
        total_cost += get_cached_dist(grid, route[i][2], route[i+1][2], bfs_shortest_path, cache, mode)
    return total_cost



#Path quality function Q(r)
def path_quality_finder(grid, route, bfs_shortest_path,cache, mode = "simple"):
    total_quality = 0
    current_time = 0
    user_qualities = {}
    #Iterate through route, calculating time taken for each leg
    for i in range(len(route)-1):
            #Increment time by path cost
            dist = get_cached_dist(grid, route[i][2], route[i+1][2], bfs_shortest_path, cache, mode) 
            current_time += dist
            #Calculate the user quality, Q(u) for a given user
            if route[i+1][1] == "dropoff":
                user_id = route[i+1][0]
                user_qualities[user_id] = current_time
                total_quality += current_time
    return total_quality, user_qualities



#Memoization cache for path and quality costs
def get_cached_dist(grid, start, end, bfs_shortest_path, cache, mode="simple"):
    # Simple mode: use Manhattan distance
    if mode == "simple":
        return get_dist(start, end)
    else:
        # Create a key for the memoization dictionary
        pair_key = tuple(sorted((start, end)))
        if pair_key in cache:
            return cache[pair_key]
        path = bfs_shortest_path(grid, start, end)
        if path is None:
            # If there is no path between the two stops, return infinity
            return float('inf')
        path_cost = path["length"]
        cache[pair_key] = path_cost
        return path_cost
    