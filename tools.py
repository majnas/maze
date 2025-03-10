# tools.py
from icecream import ic
class Sensor:
    def __init__(self, maze):
        self.maze = maze
    
    def read_distance(self, position, direction):
        x, y = position
        distance = 0
        x += direction[0]
        y += direction[1]
        while 0 <= x < len(self.maze.grid) and 0 <= y < len(self.maze.grid[0]) and self.maze.grid[y][x] == 0:
            distance += 1
            x += direction[0]
            y += direction[1]
        return distance
    
    def read_all_directions(self, position)->dict:
        """
        Returns distances in all four directions from the given position.
        Returns a dictionary with directions as keys and distances as values.
        """
        
        directions = {
            'up': (0, 1),       # Moving up increases y
            'down': (0, -1),    # Moving down decreases y
            'left': (-1, 0),    # Moving left decreases x
            'right': (1, 0)     # Moving right increases x
        }

        distances = {}
        for direction_name, direction_vector in directions.items():
            distances[direction_name] = self.read_distance(position, direction_vector)
        
        return distances