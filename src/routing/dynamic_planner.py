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

def dynamic_planner(all_requests, distance_cache, gamma):
    return current_state.route, current_state.total_g
