import numpy as np
from scipy.signal import convolve2d


class Grid:
    """
    Represents the grid of cells for Conway's Game of Life.

    This class manages the state of all cells and the core simulation logic
    for evolving from one generation to the next.
    """

    def __init__(self, width, height):
        """
        Initializes the grid with a given width and height.

        Args:
            width (int): The number of cells in the horizontal direction.
            height (int): The number of cells in the vertical direction.
        """
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.uint8)

    def get_cell(self, x, y):
        """
        Gets the state of a cell at a given coordinate.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.

        Returns:
            int: The state of the cell (1 for alive, 0 for dead), or 0 if
                 the coordinates are out of bounds.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y, x]
        return 0

    def set_cell(self, x, y, state):
        """
        Sets the state of a cell at a given coordinate.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
            state (int): The new state of the cell (0 or 1).
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = state

    def toggle_cell(self, x, y):
        """
        Toggles the state of a cell (alive to dead, dead to alive).

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = 1 - self.grid[y, x]

    def update(self):
        """
        Evolves the grid to the next generation based on the rules of the game.
        This implementation uses 2D convolution for highly efficient neighbor counting.
        """
        # The kernel defines the neighborhood. 1 means neighbor, 0 means self.
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

        # Use convolution to count live neighbors for each cell. 'same' mode ensures
        # the output is the same size as the input, and 'wrap' handles the toroidal
        # (wrap-around) boundaries.
        num_neighbors = convolve2d(self.grid, kernel, mode="same", boundary="wrap")

        # Apply the rules of Life:
        # A cell is born if it has 3 neighbors.
        born = (num_neighbors == 3) & (self.grid == 0)
        # A cell survives if it has 2 or 3 neighbors.
        survives = ((num_neighbors == 2) | (num_neighbors == 3)) & (self.grid == 1)

        # Update the grid state
        self.grid.fill(0)
        self.grid[born | survives] = 1

    def count_neighbors(self, x, y):
        """
        DEPRECATED: This method is no longer used in the main update loop,
        as neighbor counting is now handled efficiently by convolution.
        It is kept for potential debugging or alternative implementations.
        """
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue

                # Toroidal wrap-around logic
                neighbor_x = (x + j + self.width) % self.width
                neighbor_y = (y + i + self.height) % self.height

                if self.grid[neighbor_y, neighbor_x] == 1:
                    count += 1
        return count

    def reset(self):
        """Resets all cells on the grid to dead (0)."""
        self.grid.fill(0)

    def clear(self):
        self.grid = np.zeros((self.height, self.width), dtype=np.int8)

    def load_pattern(self, pattern, center=True):
        """
        Loads a pattern onto the grid.
        
        Args:
            pattern (list): List of (x, y) tuples representing live cells
            center (bool): Whether to center the pattern on the grid
        """
        if not pattern:
            return
            
        if center:
            # Calculate pattern bounds
            min_x = min(coord[0] for coord in pattern)
            max_x = max(coord[0] for coord in pattern)
            min_y = min(coord[1] for coord in pattern)
            max_y = max(coord[1] for coord in pattern)
            
            pattern_width = max_x - min_x + 1
            pattern_height = max_y - min_y + 1
            
            # Calculate offset to center the pattern
            offset_x = (self.width - pattern_width) // 2 - min_x
            offset_y = (self.height - pattern_height) // 2 - min_y
        else:
            offset_x = 0
            offset_y = 0
        
        # Place the pattern on the grid
        for x, y in pattern:
            grid_x = x + offset_x
            grid_y = y + offset_y
            if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
                self.grid[grid_y, grid_x] = 1
