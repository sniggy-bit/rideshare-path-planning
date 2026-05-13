#Static behavior and path planning module for rideshare application 

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
    def total_g(self):
        return self.total_t + self.total_q

#Route generator function: takes in a grid map, a set of passenger requests, and a vehicle's current location. 
# Returns an optimal path for the vehicle to pick up and drop off all passengers using A*

def route_generator(grid: Grid, requests: events.RequestSet, taxi_loc: tuple, gamma = 1.5): 
    
    #SETUP

    #Get passenger requests and their IDs
    request_dict = requests.get_all_requests()
    passenger_ids = tuple(request_dict.keys())

    #Pre-compute distances for routes, add edge cases for when passenger pick location is same as taxi location.
    distance_cache = {}
    #Get list of all stops for passengers
    stops = [(None,"start",taxi_loc)]
    for passenger_id in passenger_ids:
        pickup_location = request_dict[passenger_id].pickup_location
        dropoff_location = request_dict[passenger_id].dropoff_location
        stops.append((passenger_id, "pickup", pickup_location))
        stops.append((passenger_id, "dropoff", dropoff_location))
    distance_cache = all_distances(grid, stops, bfs_shortest_path, distance_cache, mode = "simple")

    #INITIALIZATION
    
    # 1. Identify the first passenger to satisfy WLOG
    first_p_id = passenger_ids[0]
    first_req = request_dict[first_p_id]

    # 2. Calculate the fixed cost from taxi to A
    dist_to_a = distance_cache[tuple(sorted((taxi_loc, first_req.pickup_location)))]

    # 3. Create the initial state: A is already picked up
    # Note: total_t starts at dist_to_a. total_q (quality) starts at 0 or weighted dist_to_a.
    initial_route = [("Taxi", "start", taxi_loc),(first_p_id, "pickup", first_req.pickup_location)]
    print(f"Route so far: {initial_route}")
    
    initial_state = TaxiState(
        location=first_req.pickup_location,
        waiting=tuple(p for p in passenger_ids if p != first_p_id), # A is no longer waiting
        in_car=(first_p_id,), # A is in the car
        total_t = dist_to_a,
        total_q = dist_to_a,
        time=dist_to_a,
        route=initial_route
    )

    # 4. Compute initial heuristic and set J
    h_init = calculate_heuristic(initial_state, distance_cache, request_dict, gamma)
    total_j = initial_state.total_g + h_init
    print(f"Total J = {initial_state.total_g} + {h_init} = {total_j}")

    # 5. Seed the frontier
    count = 0 # Tie-breaker
    open_set = [(total_j, count, initial_state)]
    visited = {(initial_state.location, initial_state.waiting, initial_state.in_car): initial_state.total_g}

    #Search history for the animation/visualization

    #Loop to search for optimal route
    while open_set:
        _, _, current_state = heapq.heappop(open_set)
       
       #goal-test: Check whether the current state is the goal state (all passengers dropped)
        if not current_state.waiting and not current_state.in_car:
            return current_state.route
        
        #add current state to explored (closed) set:
        current_state_id = (current_state.location, current_state.waiting, current_state.in_car)
        print(f"Updated route: {current_state.route}")

        #generate child nodes and evaluate their total J values, adding them to the frontier if they haven't been explored 
        potential_next_states = generate_next_states(current_state, request_dict, distance_cache, gamma)
        print(f" Next Move options: {potential_next_states}")
        for move in potential_next_states:
            next_location, p_id, action = move
            print(f"Evaluating move {move}")
        
            #Actually getting the next locations
            if action == "pickup":
                new_waiting = tuple(p for p in current_state.waiting if p != p_id)
                new_in_car = tuple(sorted(current_state.in_car + (p_id,)))
            else: # dropoff
                new_waiting = current_state.waiting
                new_in_car = tuple(p for p in current_state.in_car if p != p_id)
            new_t, new_q = simple_cost_function(current_state, move, distance_cache, gamma)
            print(f'New T: {new_t}, New Q: {new_q}')
            next_state = TaxiState(location=next_location,
                                    waiting=new_waiting,
                                    in_car=new_in_car,
                                    total_t=new_t,
                                    total_q=new_q,
                                    route=current_state.route + [(p_id, action, next_location)]
            )
            h = calculate_heuristic(next_state, distance_cache, request_dict, gamma)
            next_state_total_j =  next_state.total_g + h

            # VERIFICATION LOGIC:
            if h < 0:
                print(f"CRITICAL ERROR: Negative heuristic at {next_state.location}")
            
            print(f'Total J = {next_state.total_g} + {h} = {next_state_total_j}')
            
            #Ensure that cycling is avoided by checking whether this is the best path to this state so far
            state_id = (next_state.location, next_state.waiting, next_state.in_car)

            if (state_id not in visited) or (next_state.total_g < visited[state_id]):
                visited[state_id] = next_state.total_g
                count += 1 # Ensure you increment your tie-breaker
                heapq.heappush(open_set, (next_state_total_j, count, next_state))
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
    
    #Calculate the wait times and ride times for remaining passengers to estimate h(u)
    pickups = {request_dict[p_id].pickup_location for p_id in state.waiting}
    dropoffs = {request_dict[p_id].dropoff_location for p_id in state.in_car}

    #Get all locations and return 0 if goal state is the next state
    all_locs = pickups.union(dropoffs)
    if not all_locs: return 0
    
    #Heuristic to estimate remaining travel time
    h_t = max(distance_cache[tuple(sorted((state.location,loc)))]for loc in all_locs)

    #Heuristic to estimate loss of quality for other users
    total_h_q = 0

    for p_id in state.waiting:

        #Estimate quality for the entire travel of the passenger, i.e curr-pickup + pickup-dropoff
        h_wait = distance_cache[tuple(sorted((state.location, request_dict[p_id].pickup_location)))]
        h_drop = distance_cache[tuple(sorted((request_dict[p_id].pickup_location, request_dict[p_id].dropoff_location)))]
        
        #Update the heuristic scores for passengers waiting
        total_h_q += (gamma * h_wait) + h_drop 

    for p_id in state.in_car:
        
        h_ride = distance_cache[tuple(sorted((state.location, request_dict[p_id].dropoff_location)))]
        
        #Update the heuristic scores for passengers in the car
        total_h_q += h_ride

    #Combine heuristics for time and quality into a single heuristic score
    print(f"Heuristic score for move: h_t {h_t} + h_q {total_h_q}")
    return h_t + total_h_q

    