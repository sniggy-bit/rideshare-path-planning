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
    from src.routing.route_evaluator import path_cost_finder,path_quality_finder
    from src.graph.path_finder import bfs_shortest_path
    from src.graph.grid import Grid
    from src.routing.static_planner import is_valid_sequence, route_generator
    from src.routing.events import RideRequest, RequestSet

    # Create a simple grid and valid_routes for testing
    grid = Grid(10, 10)

    # Create some ride requests
    requests = RequestSet()
    requests.add_request(RideRequest("A", (0, 0), (0, 5)))
    requests.add_request(RideRequest("B", (5, 0), (5, 5)))

    valid_routes = route_generator(grid, requests)

    #Initialize a memo (dict) to store previously computed costs
    dist_cache = {}
    
    print(f"{'Route Sequence':<60} | {'T(r)':<5} | {'Q(r)':<5}")
    print("-" * 75)
    
    #Test the path cost finder on the generated valid routes
    results = []
    for route in valid_routes:
        #Calculate path cost for the route using the path cost finder
        path_cost = path_cost_finder(grid, route, bfs_shortest_path, dist_cache,mode = "simple")
        #Calculate path quality for the route using the path quality finder
        path_quality, user_qualities = path_quality_finder(grid, route, bfs_shortest_path, dist_cache, mode = "simple")
        results.append({"route": route, 
                        "path_cost": path_cost, 
                        "path_quality": path_quality, 
                        "user_qualities": user_qualities})
        # Format route for printing: e.g., (A, pickup) -> (B, pickup)
        route_str = " -> ".join([f"({r[0]},{r[1]})" for r in route])
        print(f"{route_str:<60} | {path_cost:<5} | {path_quality:<5}")

    #Find the best routes based on path quality (lowest) and path cost (lowest) print it
    print("-" * 75)
    best_cost_route = min(results, key=lambda x: x['path_cost'])
    print(f"Best cost route: {best_cost_route['route']}")
    best_quality_route = min(results, key=lambda x: x['path_quality'])
    print(f"Best quality route: {best_quality_route['route']}")

    #Show that best cost route and best quality route are not infact the same
    assert best_cost_route['route'] != best_quality_route['route'], "Best cost and quality happen to be same for this case"
