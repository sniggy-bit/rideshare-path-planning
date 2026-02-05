#Tests the routing algorithms and event handling for static ride requests

import numpy as np
from src.routing.events import RideRequest, RequestSet

def test_add_and_retrieve_requests():
    request_set = RequestSet()
    
    # Create some ride requests
    request1 = RideRequest("P1", (0, 0), (2, 2))
    request2 = RideRequest("P2", (1, 1), (2, 0))
    
    # Add requests to the set
    request_set.add_request(request1)
    request_set.add_request(request2)
    
    # Retrieve all requests
    all_requests = request_set.get_all_requests()
    
    # Assertions to verify correctness
    assert len(all_requests) == 2
    assert request1.passenger_id in all_requests
    assert request2.passenger_id in all_requests

    print(all_requests)