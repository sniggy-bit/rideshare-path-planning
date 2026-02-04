#Test the static example for rideshare path planning
import numpy as np
from src.simulation.visualization import visualize_bfs
from src.graph.bfs import bfs_shortest_path
from src.graph.grid import Grid

def test_static_example():
    grid = Grid(width = 3, height = 3)
    start = (0, 0)
    target = (2, 2)

    # Define grid size
    width, height = grid.width, grid.height

    # Create a 2D numpy array to represent the grid 
    grid_array = np.zeros((width, height))

    # Find the shortest path using BFS
    path = bfs_shortest_path(start, target,grid.get_neighbors)

    # Visualize the result
    visualize_bfs(grid_array, path["path"], start, target)

    # Validate the path
    print("Computed Path: ", path["path"], "Computed Length: ", path["length"])

test_static_example()