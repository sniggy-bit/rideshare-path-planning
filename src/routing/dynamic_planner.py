#Dynamic planning module for rideshare path planning application
#Key changes from the static planning part include dynamic user requests, running A* from request to request for a given trip

#Imports
import itertools
import heapq
from src.routing import events
from src.routing.route_evaluator import all_distances, simple_cost_function
from src.graph.path_finder import bfs_shortest_path
from src.graph.grid import Grid 
from typing import List, Tuple
from src.routing.static_planner import TaxiState 

def dynamic_planner(all_requests, passenger_ids, distance_cache, taxi_loc, gamma):

    time_elapsed = 0
    passengers_waiting = []
    passengers_in_car = []

    j_old_remaining = 0
    active_route = []
    current_state = TaxiState(taxi_loc,
                              tuple(passengers_waiting),
                              tuple(passengers_in_car),
                              total_t = 0, 
                              total_q = 0, 
                              time_elapsed,
                              active_route)

    
    return total_cost
    