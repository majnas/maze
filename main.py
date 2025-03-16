# main.py
import time
import re
import json
from maze import Maze
from sensor import Sensor
from toolbox import ToolBox
from icecream import ic
from visualization import MazeVisualizer
import argparse

from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage

import os
os.environ["XDG_SESSION_TYPE"] = "xcb"



def main(args):
    maze = Maze(grid_size=args.grid_size, num_obstacles=args.num_obstacles)

    # Create a MazeVisualizer instance
    visualizer = MazeVisualizer(maze)

    sensor = Sensor(maze)
    toolbox = ToolBox(maze=maze, sensor=sensor)
    tools_descriptions = toolbox.get_tools_descriptions

    # Initialize the Chat Model.
    llm = ChatOpenAI(model="gpt-3.5-turbo")

    
    current_position = "0,0"
    target = f"{args.grid_size-1},{args.grid_size-1}"
    path = [current_position]
    
    # Create a blocked matrix (0: unexplored, 1: blocked)
    blocked_matrix = [[0 for _ in range(args.grid_size)] for _ in range(args.grid_size)]
    
    # Initial visualization.
    visualizer.display_maze([tuple(map(int, current_position.split(",")))])
    time.sleep(1)

    # Structured query as a dict
    user_prompt = (
            f"You are a robot in a {args.grid_size}x{args.grid_size} maze with obstacles. "
            f"Your goal is to reach {target} starting from 0,0. "
            f"You are currently at {current_position}"
            f"Make progress toward {target} in each step, using provided tools to avoid obstacles. "
            f"Take your time and break down the problem to solve it."
            f"botom-left is 0,0 position and top-right is {args.grid_size},{args.grid_size} position."
            f"No furture movement is needed when current_position is {args.grid_size},{args.grid_size}."
            f"I am ready to tell me which tool should I call at first step."
    )
    messages = [HumanMessage(content=user_prompt)]


    # Loop until the agent reaches the target.
    step = 1
    while current_position != target:
        print("----------------------------------------------------------")
        ic(step)
        # Build a summary of blocked positions.
        # blocked_positions = []
        # for i in range(args.grid_size):
        #     for j in range(args.grid_size):
        #         if blocked_matrix[i][j] == 1:
        #             blocked_positions.append(f"{i},{j}")
        # blocked_summary = ", ".join(blocked_positions) if blocked_positions else "None"
        
        # history_str = ", ".join(path)
        # ic(target)
        # ic(current_position)
        # ic(history_str)
        # ic(blocked_summary)
        

        ic(messages)
        response = llm.invoke(input=messages, functions=tools_descriptions)
        ic(response)

        function_call = response.additional_kwargs.get("function_call")
        if function_call:
            ic(function_call)
            function_name = function_call["name"]
            arguments = json.loads(function_call["arguments"])
            result = toolbox.get_tools_dict[function_name](**arguments)
            new_messages = toolbox.get_tools_call_content_dict[function_name](**dict(function_result=result))
            ic(function_name, arguments, result, new_messages)
            messages.extend(new_messages)
            if function_name == 'move_tool':
                current_position = result.get('new_position', current_position)
                ic(result, current_position)
                path.append(current_position)
        else:
            break


        visualizer.display_maze([tuple(map(int, current_position.split(",")))])
        time.sleep(1)

        step += 1        

    print("----------------------------------------------------------")
    for msg in messages:
        ic(msg.content)
    print("Final Path:", path)

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description='Grid configuration')

    # Add arguments
    parser.add_argument('--grid_size', 
                    type=int, 
                    default=4, 
                    help='Size of the grid (default: 4)')
    parser.add_argument('--num_obstacles', 
                    type=int, 
                    default=5, 
                    help='Number of obstacles (default: 5)')

    # Parse arguments
    args = parser.parse_args()
    main(args)
