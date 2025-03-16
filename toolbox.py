# agent_tools.py
from langchain.tools import tool
import json
from icecream import ic
from langchain.schema import HumanMessage, AIMessage, ChatMessage


class ToolBox():
    def __init__(self, maze, sensor):
        self.maze = maze
        self.sensor = sensor

    def get_tools(self):
        return [self.create_move_tool(), 
                self.create_sensor_tool()]

    @property
    def get_tools_dict(self):
        return {"move_tool": self.move_function, 
                "sensor_tool": self.sensor_function}

    @property
    def get_tools_descriptions(self):
        return [self.move_tool_description, 
                self.sensor_tool_description]

    @property
    def get_tools_call_content_dict(self):
        return {"move_tool": self.move_function_result_content, 
                "sensor_tool": self.sensor_function_result_content}

    @property
    def move_tool_description(self):        
        return {
                "name": "move_tool",
                "description": "Moves the agent in the maze based on the current position, direction, and number of steps",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "current_position": {
                            "type": "string",
                            "description": "The current position of the agent in the maze, e.g. '0,0'"
                        },
                        "direction": {
                            "type": "string",
                            "enum": ["up", "down", "left", "right"],
                            "description": "The direction to move in: 'up', 'down', 'left', or 'right'"
                        },
                        "steps": {
                            "type": "integer",
                            "description": "The number of steps to move in the specified direction (default is 1)",
                            "default": 1
                        }
                    },
                    "required": ["current_position", "direction"]
                }
            }
    
    @property
    def sensor_tool_description(self):
        return {
            "name": "sensor_tool",
            "description": "Returns sensor readings from the current position in the maze",
            "parameters": {
                "type": "object",
                "properties": {
                    "current_position": {
                        "type": "string",
                        "description": "The current position of the agent in the maze, e.g. '0,0'"
                    }
                },
                "required": ["current_position"]
            }
        }


    # Define the function separately
    def sensor_function(self, current_position: str) -> dict:
        """
        Returns sensor readings from the current position.

        The current_position should be a string representing the current position (e.g., "0,0").

        Returns a dictionary with sensor readings in all four directions.
        """
        pos = tuple(map(int, current_position.split(",")))
        readings: dict = self.sensor.read_all_directions(pos)
        readings.update(dict(current_position=current_position))
        return readings

    # Define the tool creation method
    def create_sensor_tool(self):
        # Apply the @tool decorator to the standalone function, binding it with self
        @tool
        def wrapped_sensor_function(input: str) -> dict:
            return self.sensor_function(input, self)
        return wrapped_sensor_function

    def sensor_function_result_content(self, function_result: dict)->str:
        current_position = function_result.get("current_position")
        function_result = {k:v for k,v in function_result.items() if v!=0 and k!="current_position"}
        content = f"Sensor reading at position = {current_position}: "
        if len(function_result.keys()) == 0:
            content += f"The robot stuck, and cannot move anymore."
            return [AIMessage(content=content), 
                    HumanMessage(content="Use sensor_tool to figure it out which direction is better to move.")]
        elif len(function_result.keys()) == 1:
            direction, steps = next(iter(function_result.items()))
            content += f"The robot can only move {steps} step in {direction} direction. "
            return [AIMessage(content=content), 
                    HumanMessage(content="Now use move_tool to move the robot in desire direction to reach the target.")]
        else:
            content += f"The robot can move"
            choices = list(function_result.items())
            for direction, steps in choices[:-1]:
                 new_position, _, _ = self.get_new_position(current_position, direction, steps)
                 content += f", {steps} {"step" if steps == 1 else "steps"} in {direction} direction to get to {new_position} position"
            direction, steps = choices[-1]
            new_position, _, _ = self.get_new_position(current_position, direction, steps)
            content += f" or {steps} {"step" if steps == 1 else "steps"} in {direction} direction to get to {new_position} position."

            return [AIMessage(content=content), 
                    HumanMessage(content="Now use move_tool to move the robot in desire direction to reach the target.")]

    def get_new_position(self, 
                      current_position: str,
                      direction: str,
                      steps: int = 1):
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
            if (0 <= candidate[0] < self.maze.grid_size and
                0 <= candidate[1] < self.maze.grid_size and
                self.maze.grid[candidate[1]][candidate[0]] == 0):
                x, y = candidate
                intermediate_positions.append(f"{x},{y}")
            else:
                blocked_position = candidate
                break
        new_position = f"{x},{y}"
        return new_position, intermediate_positions, blocked_position 


    # Define the function separately
    def move_function(self, 
                      current_position: str,
                      direction: str,
                      steps: int = 1) -> dict:
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
        new_position, intermediate_positions, blocked_position = self.get_new_position(current_position, direction, steps)
        ret = {"current_position": current_position,
               "new_position": new_position, 
               "intermediate_positions": intermediate_positions}
        if blocked_position is not None:
            ret["blocked_position"] = f"{blocked_position[0]},{blocked_position[1]}"
        return ret

    # Define the tool creation method
    def create_move_tool(self):
        # Apply the @tool decorator to the standalone function, binding it with self
        @tool
        def wrapped_move_function(current_position: str, direction: str, steps: int) -> dict:
            return self.move_function(self, current_position, direction, steps)
        return wrapped_move_function

    def move_function_result_content(self, function_result: dict)->str:
        current_position = function_result.get("current_position", "")
        new_position = function_result.get("new_position", "")
        # intermediate_positions = function_result.get("intermediate_positions", "")
        blocked_position = function_result.get("blocked_position", "")
        content = ""
        if current_position != new_position:
            content += f"The robot moved from {current_position} to {new_position} and current_position={new_position}. " 
        else:
            content += f"The robot still is in {current_position} position. " 

        if blocked_position:
            content += f"Following positions are blocked, {blocked_position}."
        return [AIMessage(content=content), HumanMessage(content="Based on current_position use sensor_tool to figure it out which direction is better to move.")]
