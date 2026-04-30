#Visualization of modified A* in the routing module

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
# Import your actual code here
from src.routing.static_planner import route_generator, TaxiState

def animate_search(grid, requests, taxi_start, final_route, search_history):
    fig, ax = plt.subplots(figsize=(10, 10))
    #Remember, 0,0 is at the top
    ax.invert_yaxis()

    # Move the X-axis to the top to match standard matrix/top-origin layouts
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    
    # --- GRID SETUP ---
    # Set the ticks to be at every integer
    ax.set_xticks(np.arange(-1, grid.width + 1, 1))
    ax.set_yticks(np.arange(-1, grid.height + 1, 1))
    
    # Show grid lines. 'both' refers to major and minor ticks.
    # We use zorder=0 to keep lines behind the markers.
    ax.grid(which='both', color='gray', linestyle='-', linewidth=0.5, alpha=0.5, zorder=0)

    #---LABEL AXES---
    ax.set_xlabel("x distance (meters)")
    ax.set_ylabel("y_distance (meters)")

    # --- PASSENGER LABELS ---
    req_dict = requests.get_all_requests()
    for p_id, req in req_dict.items():
        py,px = req.pickup_location
        # Label Pickups
        ax.scatter(*req.pickup_location, c='lime', marker='o', s=200, edgecolors='black', zorder=5)
        ax.text(req.pickup_location[0], req.pickup_location[1] + 0.3, f"Pick {p_id} {(px,py)}", 
                ha='center', fontweight='bold', fontsize=9, bbox=dict(facecolor='white', alpha=0.6))
        
        # Label Dropoffs
        ax.scatter(*req.dropoff_location, c='red', marker='x', s=100, zorder=5)
        ax.text(req.dropoff_location[0], req.dropoff_location[1] + 0.3, f"Drop {p_id} {(px,py)}", 
                ha='center', fontweight='bold', fontsize=9, bbox=dict(facecolor='white', alpha=0.6))

    # --- ANIMATION ELEMENTS ---
    #Showing explored nodes of A*
    explored_scatter = ax.scatter([], [], c='cyan', s=100, alpha=0.7, label='States Explored', zorder=50)
    #Showing the taxi (agent) itself
    taxi_marker, = ax.plot([], [], 'gold', marker='s', markersize=15, markeredgecolor='black', zorder=10)
    #Showing the actual path of the taxi
    path_line, = ax.plot([], [], 'blue', alpha=0.6, linewidth=2, label='Final Path')

    # 3. The Moving Parts
    # Initialize empty lists to store the path as it grows

    hx, hy = [], []

    def init():
        taxi_marker.set_data([], [])
        path_line.set_data([], [])
        return taxi_marker, path_line

    explored_coords = []

    def update(frame_idx):
        #Get stop from the final route index by index
        p_id, action, loc = final_route[frame_idx]
        curr_y, curr_x = loc
        
        # Append the new coordinates to our tracking lists
        hx.append(loc[0])
        hy.append(loc[1])
    
        # Update the visual elements
        taxi_marker.set_data([loc[0]], [loc[1]])
        path_line.set_data(hx, hy)

        # Show the A* search history up to this point in time

        # Since search_history is small, let's show 
        # more nodes per frame so the cyan dots stay visible.
        # This shows the first 3 explored nodes, then 6, then 9...
        current_limit = min((frame_idx + 1) * 3, len(search_history)) 
        
        # Extract the tuples
        current_cloud = [(step['pos'][1],step['pos'][0]) for step in search_history[:current_limit]]
        
        #Now add the explored coordinates to the scatter
        if current_cloud:
            points = np.array(current_cloud)
            explored_scatter.set_offsets(points)
            print(f"Frame {frame_idx}: Plotting {len(points)} dots") # <--- Debugging line

        ax.set_title(f"Step {len(hx) - 1}: {action} Passenger {p_id}")
        
        return taxi_marker, path_line, explored_scatter, ax.title

    ani = FuncAnimation(fig, update, frames= range(len(final_route)), init_func=init, 
                        blit=False, interval=5000, repeat=False)
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()