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
    def __init__(self, location:tuple, waiting:tuple, in_car:tuple, total_t=0, total_q=0, time=0, route=None):
        self.location = location        #Current location of the taxi (tuple)
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
    
    #Initialize state of taxi when the ride starts, pick up A
    start = request_dict[passenger_ids[0]]
    route = [(passenger_ids[0], "pickup", start.pickup_location)]
    #node representation: (location, waiting passengers, passengers in car, total T = 0 and total Q = 0)
    initial_state = TaxiState(location=start.pickup_location, 
                              waiting=passenger_ids, 
                              in_car=(start[0]), 
                              total_t=0, 
                              total_q=0, 
                              time=0, 
                              route=route)
    
    #A* SEARCH ###FIX BELOW###
    
    #frontier -> priority queue ordered by total J = T + Q + h(route) + h(quality))
    open_set = [(initial_state.total_j, initial_state)]
    
    #explored -> Tracks visited states to avoid cycling 
    # links state to total cost to get there.
    #in case a more efficient path to prev visited stated is found, the state can be added back to
    #frontier with updated total J in constant time
    visited = {(initial_state.location, initial_state.waiting, initial_state.in_car): initial_state.total_j}

    #Loop to search for optimal route
    while open_set:
        current_state = heapq.heappop(open_set)
       
       #goal-test: Check whether the current state is the goal state (all passengers dropped)
        if current_state.waiting == () and current_state.in_car == ():
            return current_state.route
        
        #add current state to explored (closed) set:
        current_state_id = (current_state.location, current_state.waiting, current_state.in_car)
        visited[current_state_id] = current_state.total_j
        
        #generate child nodes and evaluate their total J values, adding them to the frontier if they haven't been explored 
        potential_next_states = generate_next_states(current_state, request_dict, distance_cache, gamma)
        for move in potential_next_states:
            next_location, p_id, action = move
            if action == "pickup":
                new_waiting = tuple(p for p in current_state.waiting if p != p_id)
                new_in_car = tuple(sorted(current_state.in_car + (p_id,)))
            else: # dropoff
                new_waiting = current_state.waiting
                new_in_car = tuple(p for p in current_state.in_car if p != p_id)
            new_t, new_q = simple_cost_function(current_state, move, distance_cache, gamma)
            next_state = TaxiState(location=next_location,
                                    waiting=new_waiting,
                                    in_car=new_in_car,
                                    total_t=new_t,
                                    total_q=new_q,
                                    route=current_state.route + [move]
            )
            h = calculate_heuristic(next_state, distance_cache, request_dict, gamma)
            next_state.total_j = next_state.total_t + next_state.total_q + h
            #Ensure that cycling is avoided by checking whether this is the best path to this state so far
            state_id = (next_state.location, next_state.waiting, next_state.in_car)

            if (state_id not in visited) or ((next_state.total_j,next_state) not in open_set):
            #Update current state in frontier containing total J value
                heapq.heappush(open_set, (next_state.total_j, next_state))
            elif next_state.total_j < visited[state_id]:
                heapq.heappush(open_set, (next_state.total_j, next_state))
    #if frontier is empty and goal state doesn't exist, return failure
    return None

#Helper function to generate valid next states from the current state,
#based on the distance cache and gamma weighting factor for user quality

#Similar to get neighbors in a bfs/djikstra
#For each waiting passenger, we can generate a state where they are picked up
#For each passenger in the car, we generate a state where they are dropped off

#generates the child nodes for current state
def generate_next_states(current_state, request_dict, distance_cache, gamma):
    next_states = []
    #Generate states for picking up or dropping off each passenger
    for passenger_id in current_state.waiting:
        next_states.append((request_dict[passenger_id].pickup_location, passenger_id, "pickup"))
    for passenger_id in current_state.in_car:
        next_states.append((request_dict[passenger_id].dropoff_location, passenger_id, "dropoff"))
    return next_states

def calculate_heuristic(state:TaxiState, distance_cache, request_dict,gamma):
    #Heuristic function to estimate remaining cost to goal
    #Can be based on distance to remaining pickups/dropoffs and user quality
    heuristic_scores = {passenger_id: (0,0) for passenger_id in (state.waiting + state.in_car)}
    #make dicts of user qualities for remaining passengers remaining in car and waiting to be picked up
    h_wait = {}
    h_ride = {}
    
    #Calculate heuristics h(r) and h(u) based on distance to remaining pickups and dropoffs
    #Calculate the wait times and ride times for remaining passengers to estimate h(u)
    for passenger_id in state.waiting:
        pickup_location = request_dict[passenger_id].pickup_location
        dropoff_location = request_dict[passenger_id].dropoff_location
        #Calculate h(r) as the distance to pickup
        heuristic_t = distance_cache[(state.location, pickup_location)]
        #Calculate h(u) as the weighted wait time
        #assume min(wait time) = dist(curr,pickup) 
        h_wait[passenger_id] = distance_cache[(state.location, pickup_location)]
        heuristic_q = gamma * h_wait[passenger_id]
        #Update the heuristic values for passengers waiting 
        current_t, current_q = heuristic_scores[passenger_id]
        heuristic_scores[passenger_id] = (current_t + heuristic_t, current_q + heuristic_q)

    for passenger_id in state.in_car:
        dropoff_location = request_dict[passenger_id].dropoff_location
        #assume min(ride time) = dist(curr,dropoff)
        heuristic_t = distance_cache[(state.location, dropoff_location)] 
         #Calculate h(u) as the weighted ride time
         #assume min(ride time) = dist(curr,dropoff)
        h_ride[passenger_id] = distance_cache[(state.location, dropoff_location)]
        heuristic_q = h_ride[passenger_id]
        #Update the heuristic values for passengers in the car
        current_t, current_q = heuristic_scores[passenger_id]
        heuristic_scores[passenger_id] = (current_t + heuristic_t, current_q + heuristic_q)
    #Combine heuristics for time and quality into a single heuristic score
    total_heuristic_score = sum(t + q for t, q in heuristic_scores.values())
    return total_heuristic_score



    