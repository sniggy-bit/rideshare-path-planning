#Tests the routing algorithms and event handling for static ride requests

import numpy as np
import pytest
import random
from src.routing.events import RideRequest, RequestSet
from src.graph.grid import Grid

def test_route_generation():
    # This test will check if the static planner generates valid routes for a given set of requests
    # For simplicity, we will just check if the generated sequences are valid according to the constraints

    from src.routing.static_planner import static_planner

    # Create a grid map (for now, we can use a simple representation)
    grid_map = np.zeros((2, 2))  # 2x2 grid

    # Create some ride requests
    request_set = RequestSet()
    request_set.add_request(RideRequest("A", (0, 0), (2, 2)))
    request_set.add_request(RideRequest("B", (1, 1), (2, 0)))
    request_set.add_request(RideRequest("C", (0, 1), (1, 0)))

    # Generate routes using the static planner
    valid_routes = static_planner(grid_map, request_set)
    #print(valid_routes)
    # Assertions to verify that all generated routes are valid
    for route in valid_routes:
        assert route[0][0] == 'A'
        assert route[0][1] == 'pickup'
        passenger = route[1][0]
        if passenger == 'B' or passenger == 'C': 
            assert route [1][1] == 'pickup'

def test_route_evaluator():
    
    from src.graph.path_finder import bfs_shortest_path
    from src.routing.static_planner import route_generator

    # Create a simple grid and valid_routes for testing
    grid = Grid(10, 10)

    # Create some ride requests
    requests = RequestSet()
    requests.add_request(RideRequest("A", (0, 0), (0, 5)))
    requests.add_request(RideRequest("B", (5, 0), (5, 5)))

    #Test the route generator upto the point of caching distances
    route_generator(grid, requests)

def test_generate_next_states():
    from src.routing.static_planner import generate_next_states, TaxiState
    from src.routing.events import RideRequest, RequestSet

    # Create some ride requests
    requests = RequestSet()
    
    requests.add_request(RideRequest("A", (0, 0), (0, 5)))
    requests.add_request(RideRequest("B", (5, 0), (5, 5)))
    requests.add_request(RideRequest("C", (2, 5), (3, 3)))

    # Create a sample state for testing
    current_state = TaxiState(location=(0, 0), waiting=('C'), in_car=('A','B'), total_t=0, total_q=0, time=0)
    # Generate next states
    next_states = generate_next_states(current_state, requests.get_all_requests(), {}, gamma=1.5)
    print(f'List of next states: {next_states}')

def test_heuristic_function():
    from src.routing.static_planner import TaxiState, calculate_heuristic
    from src.routing.events import RideRequest, RequestSet
    from src.graph.path_finder import bfs_shortest_path
    from src.graph.grid import Grid
    from src.routing.route_evaluator import all_distances

    #Test grid
    grid = Grid(10, 10)

    # Create some ride requests
    requests = RequestSet()
    
    requests.add_request(RideRequest("A", (0, 0), (0, 5)))
    requests.add_request(RideRequest("B", (0, 1), (5, 5)))
    requests.add_request(RideRequest("C", (2, 5), (7, 5)))

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
    print(f"Distance cache: {distance_cache}")

    # Create a sample state for testing
    current_state = TaxiState(location=(0, 0), waiting=('B','C'), in_car=('A',), total_t=0, total_q=0, time=0)
    # Calculate heuristic value for the current state
    heuristic_value = calculate_heuristic(current_state, distance_cache, requests.get_all_requests(), gamma=1.5)
    print(f'Heuristic cost for the current state: {heuristic_value}')

def test_static_planner(benchmark):
    import random
    from src.routing.static_planner import route_generator
    from src.simulation.visualization import animate_search

    # Create a simple grid and valid_routes for testing
    grid = Grid(10, 10)

    # Create some random ride requests
    requests = RequestSet()
    users = ("A","B","C")

    for user in users:
        pickup_loc = tuple(random.randint(1,grid.height)for _ in range(2))
        drop_loc = tuple(random.randint(1,grid.height)for _ in range(2)) 
        requests.add_request(RideRequest(user, pickup_loc, drop_loc))
    #Generate start location of the taxi
    start_loc = tuple(random.randint(1,grid.height)for _ in range(2))

    # Generate routes using the static planner
    valid_route, search_history = benchmark(route_generator, grid, requests, start_loc)
    assert valid_route is not None
    assert len(search_history) > 0
    if valid_route:
        print(f'Valid route generated by the static planner: {valid_route}')
        #animate_search(grid, requests, start_loc, valid_route,search_history)


#Test with various grid sizes to check if efficiency of algorithm changes
@pytest.mark.parametrize("size", [(10,10), (50,50), (100,100)])

def test_static_planner_scales(benchmark, size):
    from src.routing.static_planner import route_generator
    
    #Generate start location of the taxi
    grid = Grid(size[0],size[1])
    start_loc = tuple(random.randint(1,grid.height)for _ in range(2))

    # Create some random ride requests
    requests = RequestSet()
    users = ("A","B","C")
    for user in users:
        pickup_loc = tuple(random.randint(1,grid.height)for _ in range(2))
        drop_loc = tuple(random.randint(1,grid.height)for _ in range(2)) 
        requests.add_request(RideRequest(user, pickup_loc, drop_loc))
    
    # This will result in 3 separate rows in your benchmark table
    benchmark(route_generator, grid, requests, (1,1))