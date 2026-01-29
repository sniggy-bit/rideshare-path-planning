#Grid class to model the 2D grid representing the city map
class Grid:
    #Constructor 
    def __init__(self, width, height) -> None:
        self.width = int(width)
        self.height = int(height)

    # Helper function to get neighbors of a node in the grid
    def get_neighbors(self, node):
        #node is a tuple (x,y). Extract x and y
        x, y = node
        neighbors = []
        # Define grid vectors: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        #Explore all directions, given they are within grid bounds
        for dx, dy in directions:
            new_x = x + dx 
            new_y = y + dy
            # Check if the new position is within grid bounds
            if (0 <= new_x < self.width) and (0 <= new_y < self.height):
                neighbors.append((new_x, new_y))
        return neighbors

