#Visualization module for rideshare path planning simulation

import matplotlib.pyplot as plt
import numpy as np


#Function to visualize BFS path on a grid
def visualize_bfs(grid, path, start, target):
    # Create grid
    fig, ax = plt.subplots()
    ax.imshow(grid, cmap='Greys', extent=[0, grid.shape[1], grid.shape[0], 0])

    # Create path (center each cell)
    rows = [p[0] + 0.5 for p in path]
    cols = [p[1] + 0.5 for p in path]
    ax.plot(cols, rows, color='red', label='BFS Path', linewidth=2)

    # Mark the start and target nodes at cell centers
    ax.scatter(start[1] + 0.5, start[0] + 0.5, color='green', s=100, label='Start')
    ax.scatter(target[1] + 0.5, target[0] + 0.5, color='blue', s=100, label='Target')

    # Draw grid lines
    ax.xaxis.set_ticks_position('top')
    ax.set_xticks(np.arange(0, grid.shape[1], 1))
    ax.set_yticks(np.arange(0, grid.shape[0], 1))

    ax.grid(True)

    ax.legend()
    plt.show(block=False)
    plt.pause(2.0) # Show the result for 2 seconds
    plt.close()    # Automatically close it so the test continues