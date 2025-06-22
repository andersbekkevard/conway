import pygame
import sys
from .config import Config
from .pattern_manager import PatternManager
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
        self.label_font = self.create_font(Config.FONT_UI_LABEL)
        self.selected_pattern = None
        self.buttons = []
        self.pattern_manager = PatternManager()
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
        """Create buttons organized in 3 columns by complexity, 4 rows."""
        categories = self.pattern_manager.get_categories_ordered()
        
        # Organize patterns by category (column)
        patterns_by_category = {}
        for category_key, category_name in categories:
            patterns = self.pattern_manager.categories[category_key].get("patterns", [])
            patterns_by_category[category_name] = patterns
        
        # Calculate grid layout: 3 columns (complexities), 4 rows
        cols = 3
        rows = 4
        
        card_width = 200
        card_height = 90
        margin_x = 30
        margin_y = 25
        header_height = 25  # Space for column headers
        
        # Center the grid perfectly on screen
        grid_width = cols * card_width + (cols - 1) * margin_x
        grid_height = rows * card_height + (rows - 1) * margin_y
        start_x = (Config.WIDTH - grid_width) // 2
        start_y = 160  # Start below instruction text + header space
        
        self.buttons = []
        self.category_labels = []  # Store column header positions
        
        # Create column headers (complexity labels)
        for col, (category_key, category_name) in enumerate(categories):
            header_x = start_x + col * (card_width + margin_x) + card_width // 2
            header_y = start_y - header_height
            self.category_labels.append((header_x, header_y, category_name))
        
        # Create pattern cards: fill columns by complexity, then rows
        for col, (category_key, category_name) in enumerate(categories):
            patterns = patterns_by_category.get(category_name, [])
            
            for row in range(rows):
                if row < len(patterns):
                    pattern_name = patterns[row]
                    
                    x = start_x + col * (card_width + margin_x)
                    y = start_y + row * (card_height + margin_y)
                    
                    description = self.pattern_manager.get_pattern_info(pattern_name)
                    card = PatternCard(
                        x, y, card_width, card_height,
                        pattern_name.replace('_', ' ').title(),  # Format display name
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
        
        # Draw category labels
        for label_x, label_y, category_name in self.category_labels:
            label_surface = self.label_font.render(category_name, True, (160, 160, 160))
            label_rect = label_surface.get_rect()
            label_rect.centerx = label_x
            label_rect.centery = label_y
            self.screen.blit(label_surface, label_rect)
        
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