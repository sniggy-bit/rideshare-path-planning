#Module containing functions to evaluate the cost and quality of a route
###UPDATE ALL FUNCTIONS IN THIS MODULE TO WORK WITH STATE REPRESENTATION IN STATIC PLANNER###

#Imports
import numpy as np
from routing.static_planner import TaxiState
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


def simple_cost_function(current_state: TaxiState, next_node, cache,gamma = 1.5):
   
    location = current_state.location    #Current location of the taxi (tuple)
    waiting = current_state.waiting          # Tuple of user IDs
    in_car = current_state.in_car            # Tuple of user IDs
    total_t = current_state.total_t         # Running T(r)
    total_q = current_state.total_q         # Running Q(u)
    total_time_elapsed = current_state.time_elapsed         # Current clock
    total_route = current_state.route         # List of actions taken so far

    user_qualities = {}
    user_pickup_times = {"A": 0}
    user_ride_times = {}

    ##TODO: Change the syntax to deal with current_state, once state is defined in the static planner
    #Also vet the logic later
    
    #Path cost T(r)
    new_t = cache[tuple(sorted((current_state.location, next_node[0])))]
    total_t += new_t
    #Path quality Q(u)
    current_time += new_t
    if next_node[2] == "pickup":
        user_id = next_node[1]
        user_pickup_times[user_id] = current_time
        print(f"User {user_id} picked up at time {current_time} seconds.")
    
    #Calculate the user quality, Q(u) for a given user
    if next_node[2]== "dropoff":
        user_id = next_node[1]
        user_ride_times[user_id] = current_time - user_pickup_times[user_id]
        print(f"User {user_id} dropped off at time {current_time} seconds.")
        print(f"Ride time: {user_ride_times[user_id]} seconds.")
        #Weight the user quality by pickup time and ride time
        user_qualities[user_id] = gamma * user_pickup_times[user_id] + user_ride_times[user_id]
    total_q = sum(user_qualities.values())
    return total_t, total_q