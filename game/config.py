class Config:
    """
    Configuration class for the Game of Life simulation.

    This class centralizes all the settings for the application,
    including screen dimensions, grid properties, UI settings.
    """

    # Screen dimensions
    WIDTH = 800
    HEIGHT = 600

    # Grid dimensions - Scaled up for complex patterns and state machines
    GRID_WIDTH = 2000
    GRID_HEIGHT = 2000
    CELL_SIZE = 3  # Smaller initial cell size for better viewport utilization

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    CELL_COLOR = WHITE
    GRID_LINE_COLOR = GRAY

    # UI settings
    BUTTON_WIDTH = 100
    BUTTON_HEIGHT = 40
    BUTTON_MARGIN = 10
    SLIDER_HEIGHT = 20
    MIN_ZOOM = 0.01  # Extended zoom-out for viewing large patterns
    MAX_ZOOM = 5.0   # Extended zoom-in for fine detail work

    # Simulation speed
    FPS = 10
    MIN_FPS = 1
    MAX_FPS = 60

    # Zoom settings
    ZOOM_STEP = 0.1

    # Font settings
    FONT_SMALL = 16
    FONT_MEDIUM = 20
    FONT_LARGE = 24
    FONT_TITLE = 36
    FONT_SUBTITLE = 18
    FONT_DESCRIPTION = 14
    FONT_BUTTON = 14      # For button text that needs to fit
    FONT_UI_LABEL = 12    # For UI labels like Speed/Zoom
