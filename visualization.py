# visualization.py
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# Use an interactive backend that supports GUI
matplotlib.use('Qt5Agg')

def display_maze(maze, path=None):
    grid_size = maze.grid_size
    grid = np.array(maze.grid)

    plt.clf()  # Clear previous frame

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xticks(np.arange(grid_size+1)-0.5, minor=True)
    ax.set_yticks(np.arange(grid_size+1)-0.5, minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=2)
    ax.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)

    # Draw obstacles
    for x in range(grid_size):
        for y in range(grid_size):
            if grid[x, y] == 1:
                ax.add_patch(plt.Rectangle((y, x), 1, 1, color='black'))

    if path:
        # Draw past path in blue
        for px, py in path[:-1]:
            ax.add_patch(plt.Circle((py + 0.5, px + 0.5), 0.3, color='blue', alpha=0.5))

        # Draw the current position in red
        x, y = path[-1]
        ax.add_patch(plt.Circle((y + 0.5, x + 0.5), 0.4, color='red'))

    plt.pause(0.5)  # Pause to show movement
    plt.show(block=False)  # Keep updating without blocking execution