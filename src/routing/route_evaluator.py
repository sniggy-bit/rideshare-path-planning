#Module containing functions to evaluate the cost and quality of a route

#Imports
import numpy as np
from src.graph.path_finder import bfs_shortest_path
from src.graph.grid import Grid

#Path cost finder function T(r): given a grid, a valid route and a bfs_shortest_path function, 
# returns the total cost of the path that goes through all the stops in the order they are given
def path_cost_finder(grid, route, bfs_shortest_path,cache,mode = "simple"):
    total_cost = 0
    if mode == "simple":
        #Simple cost function: manhattan distance between consecutive stops
        for i in range(len(route)-1):
            total_cost += get_dist(route[i][2],route[i+1][2])
        return total_cost
    else:
        for i in range(len(route)-1):
            start = route[i][2]
            end = route[i+1][2]
            #Create a key for the memoization dictionary
            pair_key = tuple(sorted((start, end)))
            
            #Check if the cost for this pair of stops has already been computed
            if pair_key in cache:
                path_cost = cache[pair_key]
            else:
                path = bfs_shortest_path(grid, start, end)
                if path is None:
                    #If there is no path between the two stops, return infinity
                    return float('inf') 
                path_cost = path["length"]
                #Store the computed cost in the memoization dictionary
                cache[pair_key] = path_cost 
            #The cost of the path is the number of edges, which is the number of nodes - 1
            total_cost += path_cost
        return total_cost
def get_dist(loc1, loc2):
    #Manhattan distance function: given two locations (x1, y1) and (x2, y2), returns the manhattan distance between them
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])

#Path quality function Q(r): given a grid, a valid route and a bfs_shortest_path function,
# returns total route quality, Q(r), and a dictionary of user qualities, Q(u) for each 
# user in the route

def path_quality_finder(grid, route, bfs_shortest_path,cache, mode = "simple"):
    current_time = 0
    user_qualities = {}
    if mode == "simple":
        #Simple cost function: manhattan distance between consecutive stops
        for i in range(len(route)-1):
            total_cost += get_dist(route[i][2],route[i+1][2])
        return total_cost
    #Iterate through route, calculating time taken for each leg
    for i in range(len(route)-1):
            start = route[i][2]
            end = route[i+1][2]
            #Create a key for the memoization dictionary
            pair_key = tuple(sorted((start, end)))
            
            #Check if the cost for this pair of stops has already been computed
            if pair_key in cache:
                path_cost = cache[pair_key]
            else:
                path = bfs_shortest_path(grid, start, end)
                
                if path is None:
                    #If there is no path between the two stops, return infinity
                    return float('inf') 
                
                path_cost = path["length"]
                #Store the computed cost in the memoization dictionary
                cache[pair_key] = path_cost 
            
            #Increment time by path cost
            current_time += path_cost
            
            #Calculate the user quality, Q(u) for a given user
            if route[i+1][1] == "dropoff":
                user_id = route[i+1][0]
                user_qualities[user_id] = current_time
    
    #Calculate route quality, Q(r), as the sum of user qualities
    total_quality = sum(user_qualities.values())
    return total_quality, user_qualities
