# maze.py
class Maze:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = self.generate_grid()

    def generate_grid(self):
        # Initialize the grid with no obstacles
        return [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
    
    def add_obstacles(self, obstacles):
        # Add obstacles to the grid
        for (x, y) in obstacles:
            self.grid[x][y] = 1