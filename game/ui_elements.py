import pygame


class Button:
    """
    A clickable UI button.
    """

    def __init__(self, x, y, width, height, text, on_click, font):
        """
        Initializes a Button instance.

        Args:
            x (int): The x-coordinate of the button.
            y (int): The y-coordinate of the button.
            width (int): The width of the button.
            height (int): The height of the button.
            text (str): The text displayed on the button.
            on_click (callable): The function to call when the button is clicked.
            font (pygame.font.Font): The font used to render the button's text.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.on_click = on_click
        self.font = font
        self.color = (100, 100, 100)
        self.text_color = (255, 255, 255)
        self.hover_color = (150, 150, 150)
        self.hovered = False

    def draw(self, screen):
        """Draws the button on the screen."""
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color

        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)  # Border
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered

    def handle_event(self, event):
        """
        Handles a pygame event. If the button is clicked, it calls the
        on_click function.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()
                return True
        return False


class Slider:
    """
    A draggable UI slider for selecting a value within a range.
    """

    def __init__(
        self, x, y, width, height, min_val, max_val, current_val, font, label=""
    ):
        """
        Initializes a Slider instance.

        Args:
            x (int): The x-coordinate of the slider.
            y (int): The y-coordinate of the slider.
            width (int): The width of the slider track.
            height (int): The height of the slider track.
            min_val (float): The minimum value of the slider.
            max_val (float): The maximum value of the slider.
            current_val (float): The initial value of the slider.
            font (pygame.font.Font): The font for the label.
            label (str, optional): A label to display above the slider. Defaults to "".
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = current_val
        self.label = label
        self.font = font
        self.handle_radius = height
        self.dragging = False

    def draw(self, screen):
        """Draws the slider and its handle on the screen."""
        # Draw slider track
        pygame.draw.rect(screen, (150, 150, 150), self.rect, border_radius=5)

        # Calculate handle position
        handle_x = (
            self.rect.x
            + ((self.value - self.min_val) / (self.max_val - self.min_val))
            * self.rect.width
        )
        handle_pos = (int(handle_x), self.rect.centery)

        # Draw handle
        pygame.draw.circle(screen, (200, 200, 200), handle_pos, self.handle_radius)

        # Draw label and value
        if self.label:
            label_text = self.font.render(
                f"{self.label}: {int(self.value)}", True, (255, 255, 255)
            )
            screen.blit(label_text, (self.rect.x, self.rect.y - 20))

    def handle_event(self, event):
        """
        Handles pygame events for the slider. Manages dragging the handle
        and updating the slider's value.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                # Jump to click position
                self.update_value_from_pos(event.pos[0])
                return True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.update_value_from_pos(event.pos[0])
                return True

        return False

    def update_value_from_pos(self, mouse_x):
        """Updates the slider's value based on the mouse's x-coordinate."""
        rel_x = max(0, min(mouse_x - self.rect.x, self.rect.width))
        self.value = self.min_val + (rel_x / self.rect.width) * (
            self.max_val - self.min_val
        )
        self.value = max(self.min_val, min(self.max_val, self.value))


class PatternCard:
    """
    A specialized button for pattern selection with integrated title and description.
    """

    def __init__(
        self, x, y, width, height, title, description, on_click, title_font, desc_font
    ):
        """
        Initializes a PatternCard instance.

        Args:
            x (int): The x-coordinate of the card.
            y (int): The y-coordinate of the card.
            width (int): The width of the card.
            height (int): The height of the card.
            title (str): The pattern name/title.
            description (str): The pattern description.
            on_click (callable): The function to call when clicked.
            title_font (pygame.font.Font): Font for the title.
            desc_font (pygame.font.Font): Font for the description.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.description = description
        self.on_click = on_click
        self.title_font = title_font
        self.desc_font = desc_font

        # Special colors for Empty pattern to signify importance
        if title == "Empty":
            self.color = (100, 100, 100)  # Lighter gray for clean/important feel
            self.hover_color = (130, 130, 130)  # Brighter gray on hover
            self.border_color = (160, 160, 160)  # Lighter gray border
        else:
            self.color = (60, 60, 60)
            self.hover_color = (90, 90, 90)
            self.border_color = (140, 140, 140)

        self.title_color = (255, 255, 255)
        self.desc_color = (180, 180, 180)

    def draw(self, screen):
        """Draws the pattern card on the screen."""
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color

        # Draw card background with square corners (matching Game of Life cells)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)

        # Draw title
        title_surface = self.title_font.render(self.title, True, self.title_color)
        title_rect = title_surface.get_rect()
        title_rect.centerx = self.rect.centerx
        title_rect.y = self.rect.y + 15
        screen.blit(title_surface, title_rect)

        # Draw description with text wrapping
        self.draw_wrapped_text(
            screen,
            self.description,
            self.desc_font,
            self.desc_color,
            self.rect.x + 10,
            title_rect.bottom + 8,
            self.rect.width - 20,
            self.rect.bottom - (title_rect.bottom + 8) - 10,
        )

    def draw_wrapped_text(self, screen, text, font, color, x, y, max_width, max_height):
        """Draw text with word wrapping within the specified bounds."""
        words = text.split(" ")
        lines = []
        current_line = []

        for word in words:
            test_line = " ".join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)  # Word is too long, add it anyway

        if current_line:
            lines.append(" ".join(current_line))

        # Draw lines
        line_height = font.get_height()
        for i, line in enumerate(lines):
            line_y = y + i * (line_height + 2)
            if line_y + line_height > y + max_height:
                break  # Don't draw lines that would exceed bounds
            line_surface = font.render(line, True, color)
            line_rect = line_surface.get_rect()
            line_rect.centerx = x + max_width // 2
            line_rect.y = line_y
            screen.blit(line_surface, line_rect)

    def handle_event(self, event):
        """
        Handles a pygame event. If the card is clicked, it calls the
        on_click function.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()
                return True
        return False
