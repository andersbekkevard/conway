class Config:
    """
    Configuration class for the Game of Life simulation.

    This class centralizes all the settings for the application,
    including screen dimensions, grid properties, UI settings.
    """

    # Screen dimensions
    WIDTH = 800
    HEIGHT = 600

    # Grid dimensions
    GRID_WIDTH = 100
    GRID_HEIGHT = 100
    CELL_SIZE = 15  # Initial cell size

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
    MIN_ZOOM = 0.1
    MAX_ZOOM = 3.0

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
