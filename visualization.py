import matplotlib.pyplot as plt
import numpy as np

class MazeVisualizer:
    def __init__(self, maze):
        self.maze = maze
        self.grid_size = maze.grid_size
        self.grid = np.array(maze.grid)
        # Create figure and axes once during initialization.
        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self._setup_axes()

    def _setup_axes(self):
        """Set up the axes properties."""
        self.ax.set_xlim(-0.5, self.grid_size - 0.5)
        self.ax.set_ylim(-0.5, self.grid_size - 0.5)
        self.ax.set_aspect('equal')  # Ensure square cells.
        self.ax.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)

    def display_maze(self, path=None):
        """Update and display the maze with an optional path."""
        # Clear the previous content.
        self.ax.cla()
        self._setup_axes()  # Reapply axes setup after clearing.

        # Draw each cell with a border and color start/finish cells differently.
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                # Set start and finish colors.
                if (x, y) == (0, 0):
                    cell_color = 'green'  # Start cell.
                elif (x, y) == (self.grid_size - 1, self.grid_size - 1):
                    cell_color = 'red'    # Finish cell.
                else:
                    cell_color = 'white' if self.grid[x, y] == 0 else 'black'

                self.ax.add_patch(plt.Rectangle(
                    (y - 0.5, x - 0.5), 1, 1,
                    facecolor=cell_color,
                    edgecolor='black', linewidth=1
                ))

        if path:
            # Draw the path in blue.
            for px, py in path[:-1]:
                self.ax.add_patch(plt.Circle((py, px), 0.3, color='blue', alpha=0.5))
            # Draw the current (robot) position as a blue circle.
            x, y = path[-1]
            self.ax.add_patch(plt.Circle((y, x), 0.4, color='blue'))

        # Update the display.
        plt.pause(0.1)

    def close(self):
        """Close the figure when done."""
        plt.close(self.fig)
