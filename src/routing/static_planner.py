#Static path planning module for rideshare application 

#For now, the module implements a bfs-based path planner on a grid map. A* will be added later once costs and heuristics are defined.

#Imports
import numpy as np
from itertools import permutations

#Static planner function
def static_planner():
    
