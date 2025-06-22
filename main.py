import pygame
import sys
from game.config import Config
from game.game_logic import GameController
from game.ui_elements import Button, Slider
from game.pattern_selection import PatternSelectionScreen


class Game:
    """
    The main class for the Conway's Game of Life application.

    This class initializes all components (Pygame, UI, game logic),
    handles the main game loop, processes user events, and manages
    the overall application state.
    """

    def __init__(self, selected_pattern=None):
        """
        Initializes the game, setting up the screen, clock, fonts,
        UI elements, and starting with the selected pattern.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        pygame.display.set_caption("Conway's Game of Life")
        self.clock = pygame.time.Clock()
        self.game_logic = GameController(selected_pattern)
        self.paused = True

        # Drawing cooldown to prevent accidental drawing after pattern selection
        self.drawing_cooldown_end = 0

        # Mouse mode: True = draw cells, False = erase cells
        self.draw_mode = True

        # Set zoom and speed to comfortable defaults for pattern observation
        self.zoom = (Config.MIN_ZOOM + Config.MAX_ZOOM) / 2
        self.current_fps = 10  # Slower default for better pattern observation

        # Camera/View attributes - center the view on the middle of the grid
        # Must calculate offset AFTER zoom is set
        grid_center_x = (Config.GRID_WIDTH * Config.CELL_SIZE) / 2
        grid_center_y = (Config.GRID_HEIGHT * Config.CELL_SIZE) / 2
        screen_center_x = Config.WIDTH / 2
        screen_center_y = Config.HEIGHT / 2

        self.offset = pygame.math.Vector2(
            grid_center_x * self.zoom - screen_center_x,
            grid_center_y * self.zoom - screen_center_y,
        )

        # Initialize fonts with better quality
        self.font = self.create_font(Config.FONT_LARGE)
        self.title_font = self.create_font(Config.FONT_TITLE)
        self.subtitle_font = self.create_font(Config.FONT_SUBTITLE)
        self.button_font = self.create_font(Config.FONT_BUTTON)
        self.ui_label_font = self.create_font(Config.FONT_UI_LABEL)

        # Create control buttons with smaller font
        (
            self.toggle_button,
            self.clear_button,
            self.new_pattern_button,
            self.mode_button,
        ) = self.create_buttons()
        self.buttons = [
            self.toggle_button,
            self.clear_button,
            self.new_pattern_button,
            self.mode_button,
        ]

        self.zoom_slider = self.create_zoom_slider()
        self.speed_slider = self.create_speed_slider()

    def create_font(self, size):
        """Create a high-quality font with fallbacks."""
        try:
            # Try to use a better system font first
            return pygame.font.SysFont("arial", size, bold=False)
        except:
            try:
                # Fallback to default font with specified size
                return pygame.font.Font(None, size)
            except:
                # Last resort - system default
                return pygame.font.SysFont(None, size)

    def create_slider(self):
        slider_width, slider_height = 150, 8
        margin = 10
        slider_x = Config.WIDTH - slider_width - margin
        slider_y = Config.HEIGHT - slider_height - margin - 10
        return Slider(
            slider_x,
            slider_y,
            slider_width,
            slider_height,
            Config.MIN_ZOOM,
            Config.MAX_ZOOM,
            self.zoom,
            self.font,
            label="Zoom",
        )

    def create_zoom_slider(self):
        """Creates and returns the zoom slider UI element."""
        slider_width = 200
        margin = 10
        slider_x = Config.WIDTH - slider_width - margin
        slider_y = Config.HEIGHT - 8 - margin
        return Slider(
            slider_x,
            slider_y,
            slider_width,
            8,
            Config.MIN_ZOOM,
            Config.MAX_ZOOM,
            self.zoom,
            self.ui_label_font,
            label="Zoom",
        )

    def create_speed_slider(self):
        """Creates and returns the speed slider UI element."""
        slider_width = 200
        margin = 10
        slider_x = Config.WIDTH - slider_width - margin
        slider_y = Config.HEIGHT - 8 - margin - 30  # Position above zoom slider
        return Slider(
            slider_x,
            slider_y,
            slider_width,
            8,
            Config.MIN_FPS,
            Config.MAX_FPS,
            self.current_fps,
            self.ui_label_font,
            label="Speed",
        )

    def create_buttons(self):
        """Creates and returns the main control buttons."""
        margin = Config.BUTTON_MARGIN
        button_width = Config.BUTTON_WIDTH
        button_height = Config.BUTTON_HEIGHT

        # Create the combined Start/Stop button
        toggle_button = Button(
            margin,
            Config.HEIGHT - button_height - margin,
            button_width,
            button_height,
            "Start",
            self.toggle_pause,
            self.button_font,
        )

        # Create the Clear button (renamed from Reset)
        clear_button = Button(
            margin + button_width + margin,
            Config.HEIGHT - button_height - margin,
            button_width,
            button_height,
            "Clear",
            self.clear_grid,
            self.button_font,
        )

        # Create the New Pattern button
        new_pattern_button = Button(
            margin + 2 * (button_width + margin),
            Config.HEIGHT - button_height - margin,
            button_width,
            button_height,
            "New Pattern",
            self.show_pattern_selection,
            self.button_font,
        )

        # Create the Draw/Erase mode toggle button
        mode_button = Button(
            margin + 3 * (button_width + margin),
            Config.HEIGHT - button_height - margin,
            button_width,
            button_height,
            "Draw",
            self.toggle_draw_mode,
            self.button_font,
        )

        return toggle_button, clear_button, new_pattern_button, mode_button

    def toggle_pause(self):
        """Toggles the simulation's paused state."""
        self.paused = not self.paused

    def toggle_draw_mode(self):
        """Toggles between draw and erase modes."""
        self.draw_mode = not self.draw_mode

    def run(self):
        """
        Runs the main game loop.

        This loop continuously handles events, updates the game state,
        and redraws the screen until the user quits.
        """
        self.panning = False

        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(int(self.current_fps))

    def handle_events(self):
        """
        Processes all user input and events, such as mouse clicks,
        key presses, and window-closing events.
        """
        mouse_pos = pygame.mouse.get_pos()

        # Handle continuous drawing/erasing when left mouse is held down
        current_time = pygame.time.get_ticks()
        if (
            pygame.mouse.get_pressed()[0]
            and self.paused
            and current_time > self.drawing_cooldown_end
        ):
            on_button = any(b.rect.collidepoint(mouse_pos) for b in self.buttons)
            on_zoom_slider = self.zoom_slider.rect.collidepoint(mouse_pos)
            on_speed_slider = self.speed_slider.rect.collidepoint(mouse_pos)
            if not on_button and not on_zoom_slider and not on_speed_slider:
                world_x = (mouse_pos[0] + self.offset.x) / self.zoom
                world_y = (mouse_pos[1] + self.offset.y) / self.zoom
                # Set cell state based on current draw mode (1 for draw, 0 for erase)
                cell_state = 1 if self.draw_mode else 0
                self.game_logic.set_cell_state(world_x, world_y, cell_state)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.speed_slider.handle_event(event):
                self.current_fps = self.speed_slider.value

            if self.zoom_slider.handle_event(event):
                new_zoom = self.zoom_slider.value

                screen_center_x = Config.WIDTH / 2
                screen_center_y = Config.HEIGHT / 2

                # Get world coordinates of the screen center before zoom
                world_center_x = (screen_center_x + self.offset.x) / self.zoom
                world_center_y = (screen_center_y + self.offset.y) / self.zoom

                self.zoom = new_zoom

                # Calculate the new offset to keep the world center at the screen center
                self.offset.x = world_center_x * self.zoom - screen_center_x
                self.offset.y = world_center_y * self.zoom - screen_center_y

            for button in self.buttons:
                if button.handle_event(event):
                    break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # Right mouse button for panning
                    self.panning = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.panning = False

            if event.type == pygame.MOUSEMOTION:
                if self.panning:
                    self.offset -= pygame.math.Vector2(event.rel)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.clear_grid()

    def update(self):
        """Updates the game state for the next frame."""
        # Update button text based on state
        self.toggle_button.text = "Start" if self.paused else "Stop"
        self.mode_button.text = "Draw" if self.draw_mode else "Erase"

        if not self.paused:
            self.game_logic.update_grid()

    def draw(self):
        """Draws all game elements to the screen."""
        self.screen.fill(Config.BLACK)
        self.game_logic.draw_grid(self.screen, self.zoom, self.offset)
        for button in self.buttons:
            button.draw(self.screen)
        self.speed_slider.draw(self.screen)
        self.zoom_slider.draw(self.screen)

    def start_game(self):
        """Starts the simulation."""
        self.paused = False

    def stop_game(self):
        """Stops the simulation."""
        self.paused = True

    def clear_grid(self):
        """Clears the grid and stops the simulation."""
        self.game_logic.reset_grid()
        self.paused = True

    def show_pattern_selection(self):
        """Shows the pattern selection screen and loads the chosen pattern."""
        pattern_screen = PatternSelectionScreen(
            self.screen, self.button_font, self.title_font, self.subtitle_font
        )
        selected_pattern = pattern_screen.run()
        if selected_pattern:
            self.game_logic.load_pattern(selected_pattern)
            self.paused = True
            # Set cooldown to prevent accidental drawing after pattern selection
            self.drawing_cooldown_end = pygame.time.get_ticks() + 300  # 300ms cooldown


def run_game():
    """Main function to run the game with pattern selection."""
    pygame.init()
    screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))

    # Create fonts for pattern selection
    def create_font(size):
        try:
            return pygame.font.SysFont("arial", size, bold=False)
        except:
            try:
                return pygame.font.Font(None, size)
            except:
                return pygame.font.SysFont(None, size)

    font = create_font(Config.FONT_LARGE)
    button_font = create_font(Config.FONT_BUTTON)
    title_font = create_font(Config.FONT_TITLE)
    subtitle_font = create_font(Config.FONT_SUBTITLE)

    # Show pattern selection screen first
    pattern_screen = PatternSelectionScreen(
        screen, button_font, title_font, subtitle_font
    )
    selected_pattern = pattern_screen.run()

    # Start the game with the selected pattern
    if selected_pattern:
        game = Game(selected_pattern)
        # Set initial cooldown to prevent accidental drawing after startup pattern selection
        game.drawing_cooldown_end = pygame.time.get_ticks() + 300  # 300ms cooldown
        game.run()

    pygame.quit()


if __name__ == "__main__":
    """The main entry point for the application."""
    run_game()
