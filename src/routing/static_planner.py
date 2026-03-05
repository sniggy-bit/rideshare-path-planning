#Static path planning module for rideshare application 

#Imports
import itertools
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
# Returns an optimal path for the vehicle to pick up and drop off all passengers using beam search with a beam 
# width of 2.
def route_generator(grid: Grid, requests: events.RequestSet, beam_width: int = 2, gamma = 1.5): 
    
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
    initial_state = TaxiState(location=(0, 0), waiting=passenger_ids, in_car=())
    
    #BEAM SEARCH
    beam = [initial_state]
    
    return


#Helper function to check if a sequence of stops is valid
def is_valid_sequence(sequence):

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
    