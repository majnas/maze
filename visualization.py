# visualization.py
import matplotlib.pyplot as plt
import numpy as np

class MazeVisualizer:
    def __init__(self, maze):
        self.maze = maze
        self.grid_size = maze.grid_size
        self.grid = np.array(maze.grid)
        # Create figure and axes once during initialization
        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self._setup_axes()

    def _setup_axes(self):
        """Set up the axes properties."""
        self.ax.set_xlim(-0.5, self.grid_size - 0.5)
        self.ax.set_ylim(-0.5, self.grid_size - 0.5)
        self.ax.set_aspect('equal')  # Ensure square cells
        self.ax.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)

    def display_maze(self, path=None):
        """Update and display the maze with an optional path."""
        # Clear the previous content
        self.ax.cla()
        self._setup_axes()  # Reapply axes setup after clearing

        # Draw each cell with a border
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                # Draw a rectangle for every cell with a border
                self.ax.add_patch(plt.Rectangle(
                    (y - 0.5, x - 0.5), 1, 1, 
                    facecolor='white' if self.grid[x, y] == 0 else 'black',
                    edgecolor='black', linewidth=1
                ))

        if path:
            # Draw the path in blue
            for px, py in path[:-1]:
                self.ax.add_patch(plt.Circle((py, px), 0.3, color='blue', alpha=0.5))
            # Draw the current position in red
            x, y = path[-1]
            self.ax.add_patch(plt.Circle((y, x), 0.4, color='red'))

        # Update the display
        plt.pause(0.1)

    def close(self):
        """Close the figure when done."""
        plt.close(self.fig)