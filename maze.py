import random
from typing import Optional

class Maze:
    def __init__(self, grid_size: int = 4, num_obstacles: Optional[int] = None):
        self.grid_size = grid_size
        self.grid = self.generate_grid()
        if num_obstacles is not None:
            self.add_random_obstacles(num_obstacles)

    def generate_grid(self):
        # Initialize the grid with no obstacles.
        return [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
    
    def add_obstacles(self, obstacles):
        # Place obstacles on the grid.
        for (x, y) in obstacles:
            self.grid[x][y] = 1

    def add_random_obstacles(self, num_obstacles):
        # Add random obstacles to the grid.
        if num_obstacles > self.grid_size * self.grid_size:
            raise ValueError("Number of obstacles exceeds available grid cells")
        
        count = 0
        while count < num_obstacles:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if x == 0 and y == 0:
                continue
            if self.grid[x][y] == 0:  # Only add an obstacle if the cell is empty.
                self.grid[x][y] = 1
                count += 1

if __name__ == "__main__":
    # Create a maze of size 4x4.
    m = Maze(grid_size=4)
    print("Initial grid:")
    print(m.grid)
    
    # Add specified obstacles.
    obstacles = [(1, 1), (2, 2), (3, 1)]  # Example obstacles.
    m.add_obstacles(obstacles)
    print("Grid after adding specified obstacles:")
    print(m.grid)
    
    # Create a new maze for demonstration of random obstacles.
    m_random = Maze(grid_size=4)
    m_random.add_random_obstacles(5)
    print("Grid after adding 5 random obstacles:")
    print(m_random.grid)
