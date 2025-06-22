import pygame
import sys
from .config import Config
from .patterns import PATTERNS, PATTERN_INFO
from .ui_elements import Button, PatternCard


class PatternSelectionScreen:
    """
    Pattern selection screen that allows users to choose from available
    Game of Life patterns before starting the simulation.
    """

    def __init__(self, screen, font, title_font=None, subtitle_font=None):
        """
        Initialize the pattern selection screen.
        
        Args:
            screen (pygame.Surface): The main game screen
            font (pygame.font.Font): Font for rendering text
            title_font (pygame.font.Font): Font for title text
            subtitle_font (pygame.font.Font): Font for subtitle text
        """
        self.screen = screen
        self.font = font
        self.title_font = title_font or self.create_font(Config.FONT_TITLE)
        self.subtitle_font = subtitle_font or self.create_font(Config.FONT_SUBTITLE)
        self.description_font = self.create_font(Config.FONT_DESCRIPTION)
        self.selected_pattern = None
        self.buttons = []
        self.create_buttons()

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

    def create_buttons(self):
        """Create buttons for each available pattern."""
        patterns = list(PATTERNS.keys())
        
        # Ensure Empty is first
        if "Empty" in patterns:
            patterns.remove("Empty")
            patterns.insert(0, "Empty")
        
        # Calculate grid layout for pattern cards
        cols = 3
        rows = (len(patterns) + cols - 1) // cols
        
        card_width = 220
        card_height = 90  # Taller cards to fit title + description
        margin_x = 20
        margin_y = 25   # Reduced since descriptions are integrated
        
        # Position grid below instruction text with proper spacing
        grid_width = cols * card_width + (cols - 1) * margin_x
        grid_height = rows * card_height + (rows - 1) * margin_y
        start_x = (Config.WIDTH - grid_width) // 2
        start_y = 140  # Start below instruction text at y=110 with 30px spacing
        
        self.buttons = []
        for i, pattern_name in enumerate(patterns):
            row = i // cols
            col = i % cols
            
            x = start_x + col * (card_width + margin_x)
            y = start_y + row * (card_height + margin_y)
            
            description = PATTERN_INFO.get(pattern_name, "")
            card = PatternCard(
                x, y, card_width, card_height,
                pattern_name,
                description,
                lambda p=pattern_name: self.select_pattern(p),
                self.font,  # Title font
                self.description_font  # Description font
            )
            self.buttons.append(card)

    def select_pattern(self, pattern_name):
        """Select a pattern and exit the selection screen."""
        self.selected_pattern = pattern_name

    def draw(self):
        """Draw the pattern selection screen."""
        self.screen.fill(Config.BLACK)
        
        # Draw title with antialiasing
        title_text = self.title_font.render("Select a Pattern", True, Config.WHITE)
        title_rect = title_text.get_rect(center=(Config.WIDTH // 2, 60))
        self.screen.blit(title_text, title_rect)
        
        # Draw instruction with better positioning
        instruction_text = self.subtitle_font.render("Click on a pattern to start the game", True, Config.WHITE)
        instruction_rect = instruction_text.get_rect(center=(Config.WIDTH // 2, 110))
        self.screen.blit(instruction_text, instruction_rect)
        
        # Draw pattern cards (with integrated descriptions)
        for card in self.buttons:
            card.draw(self.screen)

    def handle_events(self):
        """Handle events for the pattern selection screen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Handle card clicks
            for card in self.buttons:
                if card.handle_event(event):
                    return True  # Pattern selected
        
        return False

    def run(self):
        """
        Run the pattern selection screen until a pattern is chosen.
        
        Returns:
            str: The name of the selected pattern
        """
        clock = pygame.time.Clock()
        
        while self.selected_pattern is None:
            if self.handle_events():
                break
                
            self.draw()
            pygame.display.flip()
            clock.tick(Config.FPS)
        
        return self.selected_pattern