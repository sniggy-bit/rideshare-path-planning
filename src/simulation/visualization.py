#Visualization module for rideshare path planning simulation

import matplotlib.pyplot as plt
import numpy as np
from src.graph.bfs import bfs_shortest_path
from src.graph.grid import Grid
#Add visualization code to show the path in real time
import matplotlib.animation as animation
#Create custom colormap for visualization
from matplotlib.colors import ListedColormap

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

def run_visualization():

    # Create a simple grid and test the visualization

    grid = Grid(3,3)
    display_grid = np.zeros((grid.width, grid.height))

    #Colormap definition 
    # 0:white (empty), 1:black (wall), 2:cyan (frontier), 3:blue (visited), 5:red (path)
    my_colors = ["white", "black", "cyan", "blue", "red"]
    custom_cmap = ListedColormap(my_colors)

    # Setup Plot
    fig, ax = plt.subplots()
    im = ax.imshow(display_grid, cmap=custom_cmap, vmin=0, vmax=len(my_colors)-1)
    
    def update(frame_data):
        im.set_array(frame_data)
        return [im]

    # Create Animation
    # We pass the generator from the other file into 'frames'
    ani = animation.FuncAnimation(
        fig, 
        update, 
        frames = bfs_shortest_path(grid, (0,0), (2,2), display_grid), 
        interval = 30, 
        repeat = False,
        cache_frame_data = False
    )
    plt.show()