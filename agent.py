# agent.py
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from visualization import display_maze

class AIAgent:
    def __init__(self, maze, sensor):
        self.maze = maze
        self.sensor = sensor
        self.llm = ChatOpenAI(model="gpt-4o-mini")  # Initialize LLM
        self.path = [(0, 0)]  # Track the agent's path with starting position

    def navigate(self):
        position = (0, 0)  # Starting position

        while position != (self.maze.grid_size - 1, self.maze.grid_size - 1):
            sensor_readings = self.get_sensor_readings(position)
            direction, steps = self.get_direction_and_steps(sensor_readings)

            if direction in ['up', 'down', 'left', 'right']:
                # Limit steps to the maximum possible (distance - 1)
                max_steps = sensor_readings[direction] - 1
                steps = min(steps, max_steps)
                if steps <= 0:
                    print("No valid steps in the chosen direction.")
                    continue

                # Define movement delta
                delta = {
                    'up': (-1, 0),
                    'down': (1, 0),
                    'left': (0, -1),
                    'right': (0, 1)
                }[direction]

                # Move step-by-step
                for _ in range(steps):
                    new_position = (position[0] + delta[0], position[1] + delta[1])
                    if (0 <= new_position[0] < self.maze.grid_size and
                        0 <= new_position[1] < self.maze.grid_size and
                        self.maze.grid[new_position[0]][new_position[1]] == 0):
                        position = new_position
                        self.path.append(position)
                        display_maze(self.maze, self.path)
                        # Check if goal is reached
                        if position == (self.maze.grid_size - 1, self.maze.grid_size - 1):
                            break
                    else:
                        print("Move blocked by obstacle or boundary.")
                        break
            else:
                print("Invalid direction or steps received.")
                break  # Stop if LLM gives an invalid response

        return self.path

    def get_sensor_readings(self, position):
        return {
            'up': self.sensor.read_distance(position, (-1, 0)),
            'down': self.sensor.read_distance(position, (1, 0)),
            'left': self.sensor.read_distance(position, (0, -1)),
            'right': self.sensor.read_distance(position, (0, 1))
        }

    def get_direction_and_steps(self, sensor_readings):
        """Ask LLM for direction and number of steps based on sensor readings"""
        messages = [
            SystemMessage(content="You are a robot navigating a 4x4 maze to reach the bottom-right corner (3,3). You can move up, down, left, or right. Obstacles block movement."),
            HumanMessage(content=f"Sensor readings: {sensor_readings}. Each value is the number of cells until an obstacle or boundary. Choose a direction and how many steps to move (1 to sensor reading - 1). Respond with 'direction steps', e.g., 'right 2'.")
        ]
        response = self.llm.invoke(messages)
        try:
            parts = response.content.strip().lower().split()
            direction, steps = parts[0], int(parts[1])
            if direction in ['up', 'down', 'left', 'right'] and steps > 0:
                return direction, steps
        except Exception:
            pass
        return None, 0  # Return invalid move if parsing fails