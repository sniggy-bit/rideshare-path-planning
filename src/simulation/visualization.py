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
        # Correctly unpacking (y, x)
        py, px = req.pickup_location
        # Plot as (x, y)
        ax.scatter(px, py, c='lime', marker='o', s=200, edgecolors='black', zorder=5)
        # Label with (y, x) so it matches your backend data for debugging
        ax.text(px, py + 0.3, f"Pick {p_id} ({py}, {px})", 
                ha='center', fontweight='bold', fontsize=9, bbox=dict(facecolor='white', alpha=0.6))

        dy, dx = req.dropoff_location
        ax.scatter(dx, dy, c='red', marker='x', s=100, zorder=5)
        ax.text(dx, dy + 0.3, f"Drop {p_id} ({dy}, {dx})", 
                ha='center', fontweight='bold', fontsize=9, bbox=dict(facecolor='white', alpha=0.6))

    # --- ANIMATION ELEMENTS ---
    #Showing explored nodes of A*
    explored_scatter = ax.scatter([], [], c='cyan', s=40, alpha=0.3, label='States Explored', zorder=1)
    #Showing the taxi (agent) itself
    taxi_marker, = ax.plot([], [], 'gold', marker='s', markersize=15, markeredgecolor='black', zorder=10)
    #Showing the actual path of the taxi
    path_line, = ax.plot([], [], 'blue', alpha=0.8, linewidth=3, drawstyle='steps-post', label='Final Path', zorder=2)

    # 3. The Moving Parts
    # Initialize empty lists to store the path as it grows

    def init():
        taxi_marker.set_data([], [])
        path_line.set_data([], [])
        return taxi_marker, path_line

    # --- PREPARE DATA FOR ONE-BY-ONE ANIMATION ---
    animation_frames = []
    for p_id, action, loc in final_route:
        # 1. Grab all "thoughts" associated with this specific move
        current_leg_id = (loc, p_id, action)
        thinking_nodes = [s['pos'] for s in search_history if s.get('state_id') == current_leg_id]
    
        # 2. Add a 'think' frame for every single dot found
        for node in thinking_nodes:
            animation_frames.append({'type': 'think', 'pos': node, 'p_id': p_id, 'action': action})
        
        # 3. Add a 'move' frame for the actual taxi movement
        animation_frames.append({'type': 'move', 'pos': loc, 'p_id': p_id, 'action': action})

    cumulative_cloud = []
    hx, hy = [], []

    def update(frame_idx):
        frame_data = animation_frames[frame_idx]
        y, x = frame_data['pos'] # Unpack current position
    
        if frame_data['type'] == 'think':
        # Add to the growing heatmap
            cumulative_cloud.append((x, y))
            explored_scatter.set_offsets(np.array(cumulative_cloud))
            ax.set_title(f"Thinking about {frame_data['action']} {frame_data['p_id']}...")
        
        elif frame_data['type'] == 'move':
            # Extend the blue path line and move the gold box
            hx.append(x)
            hy.append(y)
            taxi_marker.set_data([x], [y])
            path_line.set_data(hx, hy)
            ax.set_title(f"DECISION: {frame_data['action']} {frame_data['p_id']}")

        return taxi_marker, path_line, explored_scatter, ax.title

    # CRITICAL: Change frames to use the new sequence length
    ani = FuncAnimation(fig, update, frames=range(len(animation_frames)), 
                    init_func=init, blit=False, interval=30, repeat=False)

    
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()