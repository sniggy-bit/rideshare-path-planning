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

    stops = []

    for request in requests.get_all_requests().values():
        stops.append((request.passenger_id,'pickup', request.pickup_location))
        stops.append((request.passenger_id,'dropoff', request.dropoff_location))
    
    print(f"Stops: {stops}")
    print(f"Number of stops: {len(stops)}")
    
    #Generate all valid sequences of stops (pickup and dropoff)
    
    sequences = list(permutations(stops))
    print(f"Total sequences: {len(sequences)}")
    print(f"Sample sequence: {sequences[0]}")
    valid_sequences = []
    
    for seq in sequences:
        if is_valid_sequence(seq):
            valid_sequences.append(seq)
    #print(f"Valid sequences: {valid_sequences}")
    print(f"Number of valid sequences: {len(valid_sequences)}")
    return valid_sequences

def is_valid_sequence(sequence):
        
        if (sequence[0][0] != 'A') or (sequence[0][1] != 'pickup'):
                return False
        picked_up = set()
        for stop in sequence:
            (passenger_id, action, location) = stop
            if action == 'pickup':
                picked_up.add(passenger_id)
            elif action == 'dropoff':
                if passenger_id not in picked_up:
                    return False 
        return True


    
