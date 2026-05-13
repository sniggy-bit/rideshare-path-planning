# Visualization of High-Level Path Planning

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
# Import your actual code here
from src.routing.static_planner import route_generator
from src.routing.events import RequestSet, RideRequest

def animate_search(grid, requests, taxi_start, final_route):
    fig, ax = plt.subplots(figsize=((grid.width)/2, (grid.height)/2))
    # Remember, 0,0 is at the top
    ax.invert_yaxis()

    # Move the X-axis to the top
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    
    # --- GRID SETUP ---
    ax.set_xticks(np.arange(-1, grid.width + 1, 1))
    ax.set_yticks(np.arange(-1, grid.height + 1, 1))
    ax.grid(which='both', color='gray', linestyle='-', linewidth=0.5, alpha=0.5, zorder=0)

    # --- LABEL AXES ---
    ax.set_xlabel("x distance (meters)")
    ax.set_ylabel("y_distance (meters)")

    # ---LABEL TAXI START----
    ax.scatter(final_route[0][2][0], final_route[0][2][1], c='gold', marker = '*', s=200, edgecolors='black', zorder=5)
    ax.text(final_route[0][2][0], final_route[0][2][1] + 1.0, f"Taxi Location: ({final_route[0][2][1]}, {final_route[0][2][0]})", 
            ha='center', fontweight='bold', fontsize=9, bbox=dict(facecolor='white', alpha=0.6))

    # --- PASSENGER LABELS ---
    req_dict = requests.get_all_requests()
    for p_id, req, loc in req_dict.items():
        # Extract coordinates for the text label
        ux, uy = req.pickup_location
        dx, dy = req.dropoff_location

        # Label Pickups
        ax.scatter(ux, uy, c='lime', marker='o', s=200, edgecolors='black', zorder=5)
        ax.text(ux, uy + 1.0, f"Pick {p_id} ({uy}, {ux})", 
                ha='center', fontweight='bold', fontsize=9, bbox=dict(facecolor='white', alpha=0.6))
        
        # Label Dropoffs
        ax.scatter(dx, dy, c='red', marker='x', s=100, zorder=5)
        ax.text(dx, dy + 1.0, f"Drop {p_id} ({dy}, {dx})", 
                ha='center', fontweight='bold', fontsize=9, bbox=dict(facecolor='white', alpha=0.6))

    # --- ANIMATION ELEMENTS ---
    # Taxi marker
    taxi_marker, = ax.plot([], [], 'gold', marker='s', markersize=15, markeredgecolor='black', zorder=10)
    # The path line connecting the stops
    path_line, = ax.plot([], [], 'blue', alpha=0.6, linewidth=2, drawstyle='steps-post', label='Planned Route')

    # Data containers for the path as it grows
    hx, hy = [], []

    def init():
        taxi_marker.set_data([], [])
        path_line.set_data([], [])
        return taxi_marker, path_line

    def update(frame_idx):
        # Get stop info from the final route
        step = final_route[frame_idx]
        print(step)

        p_id, action, loc = step
        
        # Add the stop location to the path
        hx.append(loc[0])
        hy.append(loc[1])
    
        # Update markers and lines
        taxi_marker.set_data([loc[0]], [loc[1]])
        path_line.set_data(hx, hy)

        # Update Title with current action
        ax.set_title(f"Step {frame_idx + 1}: {action.capitalize()} Passenger {p_id}")
        
        return taxi_marker, path_line, ax.title

    # Note: Interval is set shorter (500ms) because we are only jumping between stops now
    ani = FuncAnimation(fig, update, frames=range(len(final_route)), init_func=init, 
                        blit=False, interval=1000, repeat=False)
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()