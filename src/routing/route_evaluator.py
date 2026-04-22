#Module containing functions to evaluate the cost and quality of a route
###UPDATE ALL FUNCTIONS IN THIS MODULE TO WORK WITH STATE REPRESENTATION IN STATIC PLANNER###

#Imports
import numpy as np
from src.graph.path_finder import bfs_shortest_path
from src.graph.grid import Grid

#Memoization cache for path and quality costs
def get_cached_dist(grid, start, end, bfs_shortest_path, cache, mode="simple"):
    # Simple mode: use Manhattan distance
    if mode == "simple":
        return abs(start[0] - end[0]) + abs(start[1] - end[1])
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

#Cache all distances between stops to avoid redundant calculations

def all_distances(grid, stops, bfs_shortest_path,cache, mode = "simple"):
    for i in range(len(stops)):
        for j in range(i+1, len(stops)):
            start = stops[i][2]
            end = stops[j][2]
            # Manhattan distance for distances between stops
            cache[tuple(sorted((start, end)))] = get_cached_dist(grid, start, end, bfs_shortest_path, cache, mode="simple")
    return cache


def simple_cost_function(current_state, next_node, cache,gamma = 1.5):
   
    location = current_state.location    #Current location of the taxi (tuple)
    waiting = current_state.waiting          # Tuple of user IDs
    in_car = current_state.in_car            # Tuple of user IDs
    total_t = current_state.total_t         # Running T(r)
    total_q = current_state.total_q         # Running Q(u)
    total_time_elapsed = current_state.time_elapsed         # Current clock
    total_route = current_state.route         # List of actions taken so far

    # 1. Get the distance for this specific move
    # next_node[0] is the (x, y) location of the move
    leg_distance = cache[tuple(sorted((current_state.location, next_node[0])))]
    
    # 2. Update Total Driving Time (T)
    new_total_t = current_state.total_t + leg_distance
    
    # 3. Update Total Quality Cost (Q)
    # Penalize for everyone waiting and everyone currently in the car
    wait_penalty = len(current_state.waiting) * leg_distance * gamma
    ride_penalty = len(current_state.in_car) * leg_distance
    
    new_total_q = current_state.total_q + wait_penalty + ride_penalty
    
    return new_total_t, new_total_q