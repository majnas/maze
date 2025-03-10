# agent_tools.py
from langchain.tools import tool
import json
from icecream import ic

def create_move_tool(maze):
    @tool
    def move_tool(input: str) -> dict:
        """
        Moves the agent in the maze.

        The input should be a JSON string with the following keys:
            - current_position: string (e.g., "0,0")
            - direction: one of "up", "down", "left", or "right"
            - steps: integer number of steps to move

        Returns a dictionary with:
            - new_position: a string representing the final position after moving
            - intermediate_positions: a list of positions (as strings) visited along the way
            - blocked_position: (optional) a string representing the first cell that was blocked, if any.
        """
        params = json.loads(input)
        current_position = params.get("current_position")
        direction = params.get("direction")
        steps = int(params.get("steps", 1))
        
        x, y = map(int, current_position.split(","))
        direction_map = {
            'up': (0, 1),
            'down': (0, -1),
            'left': (-1, 0),
            'right': (1, 0)
        }
        delta = direction_map.get(direction, (0, 0))
        intermediate_positions = []
        blocked_position = None

        # Try moving one step at a time.
        for i in range(steps):
            candidate = (x + delta[0], y + delta[1])
            # Check if candidate is within bounds and is free.
            if (0 <= candidate[0] < maze.grid_size and
                0 <= candidate[1] < maze.grid_size and
                maze.grid[candidate[1]][candidate[0]] == 0):
                x, y = candidate
                intermediate_positions.append(f"{x},{y}")
            else:
                blocked_position = candidate
                break
        new_position = f"{x},{y}"
        ret = {"new_position": new_position, "intermediate_positions": intermediate_positions}
        if blocked_position is not None:
            ret["blocked_position"] = f"{blocked_position[0]},{blocked_position[1]}"
        return ret
    return move_tool

def create_sensor_tool(sensor):
    @tool
    def sensor_tool(input: str) -> dict:
        """
        Returns sensor readings from the current position.

        The input should be a string representing the current position (e.g., "0,0").

        Returns a dictionary with sensor readings in all four directions.
        """
        pos = tuple(map(int, input.split(",")))
        readings = sensor.read_all_directions(pos)
        return readings
    return sensor_tool
