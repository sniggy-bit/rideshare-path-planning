#Static path planning module for rideshare application 

#For now, the module implements a bfs-based path planner on a grid map. A* will be added later once costs and heuristics are defined.

#Imports
import numpy as np
from itertools import permutations
from src.routing import events
from src.graph.bfs import bfs_shortest_path
from src.graph.grid import Grid 
from typing import List, Tuple


#Static planner function: takes in a grid map, a set of passenger requests, and a vehicle's current location. Returns an optimal path for the vehicle to pick up and drop off all passengers.
def static_planner(grid_map, requests: events.RequestSet):
    #TODO: Add grid map representation

    #TODO: Enumerate all valid pickup and dropoff sequences for the given requests
    #Key constraint is that a passenger must be picked up before they can be dropped off

    #Extract pickup and dropoff locations from requests

    stops = [Tuple[str,str,events.node]]

    for request in requests.get_all_requests().values():
        stops.append((request.passenger_id,'pickup', request.pickup_location))
        stops.append((request.passenger_id,'dropoff', request.dropoff_location))

    #Generate all valid sequences of stops (pickup and dropoff)
    sequences = permutations(stops)
    valid_sequences = []

    def is_valid_sequence(sequence):
        picked_up = set()
        for stop in sequence:
            print(stop)
            (passenger_id, action, location) = stop
            if passenger_id != 'A':
                return False
            elif action == 'pickup':
                picked_up.add(passenger_id)
            elif action == 'dropoff':
                if passenger_id not in picked_up:
                    return False
        return True
    
    for seq in sequences:
        if is_valid_sequence(seq):
            valid_sequences.append(seq)
    return valid_sequences




    
