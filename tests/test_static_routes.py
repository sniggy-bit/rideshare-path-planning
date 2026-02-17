#Tests the routing algorithms and event handling for static ride requests

import numpy as np
from src.routing.events import RideRequest, RequestSet

# def test_add_and_retrieve_requests():
#     request_set = RequestSet()
#     
#     # Create some ride requests
#     request1 = RideRequest("P1", (0, 0), (2, 2))
#     request2 = RideRequest("P2", (1, 1), (2, 0))
#     
#     # Add requests to the set
#     request_set.add_request(request1)
#     request_set.add_request(request2)
#     
#     # Retrieve all requests
#     all_requests = request_set.get_all_requests()
#     
#     # Assertions to verify correctness
#     assert len(all_requests) == 2
#     assert request1.passenger_id in all_requests
#     assert request2.passenger_id in all_requests
# 
#     print(all_requests)

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
    from src.routing.route_evaluator import path_cost_finder
    from src.graph.bfs import bfs_shortest_path
    from src.graph.grid import Grid
    from src.routing.static_planner import is_valid_sequence, route_generator
    from src.routing.events import RideRequest, RequestSet

    # Create a simple grid and valid_routes for testing
    grid = Grid(3, 3)

    # Create some ride requests
    requests = RequestSet()
    requests.add_request(RideRequest("A", (0, 0), (2, 2)))
    requests.add_request(RideRequest("B", (1, 1), (2, 0)))

    valid_routes = route_generator(grid, requests)

    #Initialize a memo (dict) to store previously computed costs
    dist_cache = {}
    #Test the path cost finder on the generated valid routes
    cost = []
    for route in valid_routes:
        route_cost = path_cost_finder(grid, route, bfs_shortest_path, dist_cache)
        cost.append(route_cost)
    print(f"Costs of valid routes: {cost}")
