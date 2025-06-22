import numpy as np
import pygame
from .grid import Grid
from .config import Config
from .patterns import PATTERNS


class GameController:
    """
    Manages the game's state and logic, acting as a controller
    in the MVC pattern. It interacts with the Grid model and is
    called by the main Game view.
    """

    def __init__(self, selected_pattern=None):
        """Initializes the GameController, creating a new Grid instance."""
        self.grid = Grid(Config.GRID_WIDTH, Config.GRID_HEIGHT)
        if selected_pattern:
            self.load_pattern(selected_pattern)

    def update_grid(self):
        """Tells the grid to update to its next state."""
        self.grid.update()

    def set_cell_state(self, world_x, world_y, state):
        """
        Sets the state of a specific cell.

        Args:
            world_x (float): The x-coordinate in the world space.
            world_y (float): The y-coordinate in the world space.
            state (int): The new state of the cell (0 for dead, 1 for alive).
        """
        cell_size = Config.CELL_SIZE
        grid_x = int(world_x / cell_size)
        grid_y = int(world_y / cell_size)
        self.grid.set_cell(grid_x, grid_y, state)

    def toggle_cell(self, world_x, world_y):
        """
        Toggles the state of a specific cell.

        Args:
            world_x (float): The x-coordinate in the world space.
            world_y (float): The y-coordinate in the world space.
        """
        cell_size = Config.CELL_SIZE
        grid_x = int(world_x / cell_size)
        grid_y = int(world_y / cell_size)
        self.grid.toggle_cell(grid_x, grid_y)

    def reset_grid(self):
        """Resets the grid to an empty state."""
        self.grid.reset()

    def load_starting_pattern(self):
        """Loads the configured starting pattern onto the grid (legacy method)."""
        pattern_name = getattr(Config, 'STARTING_PATTERN', 'Empty')
        if pattern_name in PATTERNS:
            pattern = PATTERNS[pattern_name]
            self.grid.load_pattern(pattern, center=True)

    def load_pattern(self, pattern_name):
        """
        Loads a specific pattern onto the grid.
        
        Args:
            pattern_name (str): Name of the pattern to load
        """
        if pattern_name in PATTERNS:
            self.grid.reset()
            pattern = PATTERNS[pattern_name]
            self.grid.load_pattern(pattern, center=True)

    def draw_grid(self, screen, zoom, offset):
        """
        Draws the grid and its cells onto the screen.

        This method calculates which cells are visible based on the current
        zoom and offset, and renders live cells without gaps between them
        for a cleaner appearance.

        Args:
            screen (pygame.Surface): The screen to draw on.
            zoom (float): The current zoom level.
            offset (pygame.math.Vector2): The current view offset.
        """
        cell_size = Config.CELL_SIZE * zoom

        # Determine the range of visible cells to render
        start_col = int(offset.x / cell_size)
        end_col = int((offset.x + Config.WIDTH) / cell_size) + 1
        start_row = int(offset.y / cell_size)
        end_row = int((offset.y + Config.HEIGHT) / cell_size) + 1

        # Draw the live cells with extended borders to remove gaps
        for y in range(max(0, start_row), min(self.grid.height, end_row)):
            for x in range(max(0, start_col), min(self.grid.width, end_col)):
                if self.grid.get_cell(x, y) == 1:
                    # Check adjacent cells to determine if we need to extend borders
                    has_right = (x + 1 < self.grid.width and 
                               self.grid.get_cell(x + 1, y) == 1)
                    has_bottom = (y + 1 < self.grid.height and 
                                self.grid.get_cell(x, y + 1) == 1)
                    
                    # Base rectangle
                    rect_width = cell_size
                    rect_height = cell_size
                    
                    # Extend right if there's an adjacent cell
                    if has_right:
                        rect_width += 1
                    
                    # Extend down if there's an adjacent cell
                    if has_bottom:
                        rect_height += 1
                    
                    rect = pygame.Rect(
                        x * cell_size - offset.x,
                        y * cell_size - offset.y,
                        rect_width,
                        rect_height,
                    )
                    pygame.draw.rect(screen, Config.CELL_COLOR, rect)
