#Static path planning module for rideshare application 

#Imports
import itertools
import heapq
from src.routing import events
from src.routing.route_evaluator import all_distances, simple_cost_function
from src.graph.path_finder import bfs_shortest_path
from src.graph.grid import Grid 
from typing import List, Tuple

#State representation for the taxi's current status. 
#State variables: taxi location (tuple) 
# waiting passengers (tuple of user IDs) 
# passengers in car (tuple of user IDs)
#  total distance T(r) for current route
#  total Q(u) for current passengers
#  time elapsed
#  route taken so far (list of actions).

class TaxiState:
    def __init__(self, location, waiting, in_car, total_t=0, total_q=0, time=0, route=None):
        self.location = location
        self.waiting = waiting          # Tuple of user IDs
        self.in_car = in_car            # Tuple of user IDs
        self.total_t = total_t          # Running T(r)
        self.total_q = total_q          # Running Q(u)
        self.time_elapsed = time        # Current clock
        self.route = route or []        # List of actions taken so far

        @property
        def total_j(self):
            return self.total_t + self.total_q

#Route generator function: takes in a grid map, a set of passenger requests, and a vehicle's current location. 
# Returns an optimal path for the vehicle to pick up and drop off all passengers using A*

def route_generator(grid: Grid, requests: events.RequestSet, gamma = 1.5): 
    
    #SETUP

    #Get passenger requests and their IDs
    request_dict = requests.get_all_requests()
    passenger_ids = tuple(request_dict.keys())

    #Pre-compute distances for route
    distance_cache = {}
    #Get list of all stops for passengers
    stops = []
    for passenger_id in passenger_ids:
        pickup_location = request_dict[passenger_id].pickup_location
        dropoff_location = request_dict[passenger_id].dropoff_location
        stops.append((passenger_id, "pickup", pickup_location))
        stops.append((passenger_id, "dropoff", dropoff_location))
    distance_cache = all_distances(grid, stops, bfs_shortest_path, distance_cache, mode = "simple")

    #INITIALIZATION
    
    #Initialize state of taxi when the ride starts
    start = request_dict[passenger_ids[0]]
    route = [(passenger_ids[0], "pickup", start.pickup_location)]
    initial_state = TaxiState(location = start.pickup_location, waiting=passenger_ids, in_car=())
    
    #A* SEARCH 
    open_set = [initial_state]
    heap = heapq.heapify(open_set)
    
    #Tracks visited states to avoid cycling
    visited = {(initial_state.location, initial_state.waiting, initial_state.in_car): initial_state.total_j}

    #Loop to search for optimal route
    while open_set:
        current_state = heapq.heappop(open_set)

        #Check whether the current state is the goal state (all passengers dropped)
        if current_state.waiting == () and current_state.in_car == ():
            return current_state.route
    
        #Ensure that cycling is avoided by checking whether this is the best path to this state so far
        state_id = (current_state.location, current_state.waiting, current_state.in_car)
        if state_id not in visited or visited[state_id] < current_state.total_j:
            #Update current total J to be the lowest for this state
            visited[state_id] = current_state.total_j
            for next_state in valid_next_states(current_state, distance_cache, gamma):
                heapq.heappush(open_set, next_state)
    return


#Helper function to check if an action is valid (e.g. no dropping off before pickup, A must be picked up first, etc.)
def is_valid_action(sequence):
    #Ensure A is always picked up first
    if (sequence[0][0] != 'A') or (sequence[0][1] != 'pickup'):
            return False
    picked_up = set()
    #Iterate through route so far to ensure no passenger is dropped off before being picked up
    for stop in sequence:
        (passenger_id, action, location) = stop
        if action == 'pickup':
            picked_up.add(passenger_id)
        elif action == 'dropoff':
            if passenger_id not in picked_up:
                return False 
    return True
#Helper function to generate valid next states from the current state,
#based on the distance cache and gamma weighting factor for user quality
def valid_next_states(current_state, distance_cache, gamma):
    next_states = []
    
