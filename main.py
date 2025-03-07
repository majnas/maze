# main.py
from maze import Maze
from tools import Sensor
from agent import AIAgent

def main():
    grid_size = 4
    maze = Maze(grid_size)
    obstacles = [(1, 1), (2, 2), (3, 1)]  # Example obstacles
    maze.add_obstacles(obstacles)

    sensor = Sensor(maze)
    agent = AIAgent(maze, sensor)

    path = agent.navigate()  # LLM navigates the maze

    print("Final Path:", path)

if __name__ == "__main__":
    main()