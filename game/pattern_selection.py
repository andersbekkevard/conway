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
        """Create buttons for each available pattern organized by category."""
        categories = self.pattern_manager.get_categories_ordered()
        
        # Get all patterns from all categories in order
        all_patterns = []
        category_start_indices = {}
        
        for category_key, category_name in categories:
            category_start_indices[category_name] = len(all_patterns)
            patterns = self.pattern_manager.categories[category_key].get("patterns", [])
            all_patterns.extend(patterns)
        
        # Calculate grid layout: 3 columns, 4 rows
        cols = 3
        rows = 4
        total_patterns = cols * rows
        
        card_width = 200
        card_height = 90
        margin_x = 25
        margin_y = 25
        label_width = 80  # Space for category labels
        
        # Position grid below instruction text with proper spacing for labels
        grid_width = cols * card_width + (cols - 1) * margin_x
        grid_height = rows * card_height + (rows - 1) * margin_y
        start_x = (Config.WIDTH - grid_width) // 2 + label_width // 2
        start_y = 140
        
        self.buttons = []
        self.category_labels = []  # Store category label positions
        
        # Create pattern cards in 3x4 grid
        for i, pattern_name in enumerate(all_patterns[:total_patterns]):
            row = i // cols
            col = i % cols
            
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
        
        # Add category labels based on where each category starts in the grid
        for category_name, start_idx in category_start_indices.items():
            if start_idx < len(all_patterns):
                start_row = start_idx // cols
                label_x = start_x - label_width
                label_y = start_y + start_row * (card_height + margin_y) + card_height // 2
                self.category_labels.append((label_x, label_y, category_name))

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