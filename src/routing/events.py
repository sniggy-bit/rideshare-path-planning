#Module handling passengers and their pickup/dropoff events for routing

from dataclasses import dataclass
from typing import Tuple, List, Dict

# Node definition for grid points
node = Tuple[int, int]  # (row, column) representation

#Single passenger request event
@dataclass
class RideRequest:
    passenger_id: str
    pickup_location: node
    dropoff_location: node

#Class storing multiple passenger request events
class RequestSet:
    def __init__(self):
        self.requests: Dict[str, RideRequest] = {}

    #Add a new ride request
    def add_request(self, request: RideRequest):
        self.requests[request.passenger_id] = request
    
    #Retrieve the dictionary of requests for all passengers and their requests
    def get_all_requests(self) -> Dict[str, RideRequest]:
        return self.requests
    
    #Retrieve a specific request for a given passenger ID
    def get_request(self, passenger_id: str) -> RideRequest:
        return self.requests.get(passenger_id, None)
    
    #Retrieve a pickup location for a specific passenger
    def get_pickup(self, passenger_id: str) -> node:
        return self.requests[passenger_id].pickup_location                      
    
    #Retrieve a dropoff location for a specific passenger
    def get_dropoff(self, passenger_id: str) -> node:
        return self.requests[passenger_id].dropoff_location
    


