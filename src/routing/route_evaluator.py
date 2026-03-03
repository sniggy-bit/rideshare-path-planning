#Module containing functions to evaluate the cost and quality of a route

#Imports
import numpy as np
from src.graph.path_finder import bfs_shortest_path
from src.graph.grid import Grid

#Cache all distances between stops to avoid redundant calculations

def all_distances(grid, stops, bfs_shortest_path,cache, mode = "simple"):
    for i in range(len(stops)):
        for j in range(i+1, len(stops)):
            start = stops[i][2]
            end = stops[j][2]
            # Manhattan distance for distances between stops
            cache[tuple(sorted((start, end)))] = get_cached_dist(grid, start, end, bfs_shortest_path, cache, mode="simple")
    return cache



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
    user_pickup_times = {"A": 0}
    user_ride_times = {}
    #Weighting factor gamma for user quality calculation
    gamma = 1.5
    #Iterate through route, calculating time taken for each leg
    for i in range(len(route)-1):
            #Increment time by path cost
            dist = get_cached_dist(grid, route[i][2], route[i+1][2], bfs_shortest_path, cache, mode) 
            current_time += dist

            #Record the pickup time for each user
            if route[i+1][1] == "pickup":
                user_id = route[i+1][0]
                user_pickup_times[user_id] = current_time
                print(f"User {user_id} picked up at time {current_time} seconds.")

            #Calculate the user quality, Q(u) for a given user
            if route[i+1][1] == "dropoff":
                user_id = route[i+1][0]
                user_ride_times[user_id] = current_time - user_pickup_times[user_id]
                print(f"User {user_id} dropped off at time {current_time} seconds.")
                print(f"Ride time: {user_ride_times[user_id]} seconds.")
                
                #Weight the user quality by pickup time and ride time
                user_qualities[user_id] = user_pickup_times[user_id] + gamma * user_ride_times[user_id]
        
    #Calculate total quality as the sum of user qualities
    total_quality = sum(user_qualities.values())
    return total_quality, user_qualities

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

def cost_function(grid, route, bfs_shortest_path, cache, mode="simple"):
    return path_cost_finder(grid, route, bfs_shortest_path, cache, mode)