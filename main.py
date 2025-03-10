# main.py
import time
import re
from maze import Maze
from tools import Sensor
from agent import create_move_tool, create_sensor_tool
from icecream import ic
from visualization import MazeVisualizer

from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

import os
os.environ["XDG_SESSION_TYPE"] = "xcb"

def main():
    grid_size = 4
    num_obstacles = 5
    maze = Maze(grid_size=grid_size, num_obstacles=num_obstacles)

    # Create a MazeVisualizer instance
    visualizer = MazeVisualizer(maze)

    sensor = Sensor(maze)
    # Create our two tools.
    move_tool = create_move_tool(maze)
    sensor_tool = create_sensor_tool(sensor)
    tools = [move_tool, sensor_tool]
    
    # Initialize the Chat Model.
    # chat_model = ChatOpenAI(model="gpt-4o-mini")
    chat_model = ChatOpenAI(model="gpt-3.5-turbo")
    
    # Initialize the agent with our tools.
    agent = initialize_agent(
        tools=tools,
        llm=chat_model,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    current_position = "0,0"
    target = f"{grid_size-1},{grid_size-1}"
    path = [current_position]
    
    # Create a blocked matrix (0: unexplored, 1: blocked)
    blocked_matrix = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Initial visualization.
    visualizer.display_maze([tuple(map(int, current_position.split(",")))])
    time.sleep(1)
        
    # Loop until the agent reaches the target.
    while current_position != target:
        # Build a summary of blocked positions.
        blocked_positions = []
        for i in range(grid_size):
            for j in range(grid_size):
                if blocked_matrix[i][j] == 1:
                    blocked_positions.append(f"{i},{j}")
        blocked_summary = ", ".join(blocked_positions) if blocked_positions else "None"
        
        history_str = ", ".join(path)
        ic(target)
        ic(current_position)
        ic(history_str)
        ic(blocked_summary)
        
        # Structured query as a dict
        query = {
            "input": (
                f"You are a robot in a {grid_size}x{grid_size} maze with obstacles. "
                f"Your goal is to reach {target} starting from 0,0. "
                f"You are currently at {current_position}. "
                f"Your movement history is: {history_str}. "
                f"Cells that led to a blocked path: {blocked_summary}. "
                f"Use the available tools: 'sensor_tool' to get sensor readings and 'move_tool' to move. "
                f"When calling move_tool, provide a JSON string with keys: "
                f"'current_position' (e.g., '0,0'), 'direction' (one of 'up', 'down', 'left', 'right'), and 'steps' (an integer). "
                f"Do not choose a move that leads to a position in the movement history ({history_str}) or known to be blocked ({blocked_summary}). "
                f"Return a dictionary with: 'output' (latest valid position in 'x,y' format), "
                f"'intermediate_positions' (list of all positions visited in this step), "
                f"and 'blocked_position' (list of newly identified blocked positions in 'x,y' format, or empty if none). "
                f"Make progress toward {target} in each step, using sensor readings to avoid obstacles."
            )
        }
        ic(query)
        result = agent.invoke(query)
        print("Agent result:", result)
        
        result = {'input': "You are a robot in a 4x4 maze with obstacles. Your goal is to reach 3,3 starting from 0,0. You are currently at 0,0. Your movement history is: 0,0. Cells that led to a blocked path: None. Use the available tools: 'sensor_tool' to get sensor readings and 'move_tool' to move. When calling move_tool, provide a JSON string with keys: 'current_position' (e.g., '0,0'), 'direction' (one of 'up', 'down', 'left', 'right'), and 'steps' (an integer). Return the final position in your response in the format 'x,y'. Do not choose a move that leads to a position that has already been visited or known to be blocked.", 'output': '3,1'}
        # Expect the agent to return a new position in the format "x,y".
        match = re.search(r'(\d+,\d+)', result)
        if match:
            new_position = match.group(1)
            ic(new_position)
            QQ
            # If the agent did not move, try to mark the attempted cell as blocked.
            if new_position == current_position:
                print("Agent is stuck! No valid move was made.")
                # Here, you might choose to mark a direction as blocked (if you had that info).
                break
            current_position = new_position
            path.append(current_position)
            
            # If the move tool returned a blocked cell, update our blocked matrix.
            if "blocked_position" in result:
                # Try to extract the blocked cell from the agent output.
                blocked_match = re.search(r'blocked_position.*?(\d+,\d+)', result)
                if blocked_match:
                    bp = blocked_match.group(1)
                    bx, by = map(int, bp.split(","))
                    if 0 <= bx < grid_size and 0 <= by < grid_size:
                        blocked_matrix[bx][by] = 1
            
            # Update visualization.
            display_maze(maze, [tuple(map(int, pos.split(","))) for pos in path])
            visualizer.display_maze([tuple(map(int, current_position.split(",")))])

            time.sleep(1)
        else:
            print("Failed to parse agent result. Exiting.")
            break

    print("Final Path:", path)

if __name__ == "__main__":
    main()
