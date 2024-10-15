import pygame
import time
from typing import Optional


class HUD:
    # Constants.
    DISPLAY_TIME = 3    # HUD fully visible for 3 seconds
    FADE_TIME = 1       # 1 second to fade out
    RADIUS = 11         # Your preferred radius
    FONT_SIZE = 28      # Your preferred font size
    Y_OFFSET = 8        # Your preferred offset from the bottom
    PADDING = 20        # Padding inside HUD

    surface: Optional[pygame.Surface] = None
    width = 0
    height = 0
    timer:float = 0
    hud_alpha = 0
    dirty = False
    font: Optional[pygame.font.Font] = None


    def __init__(self):
        self.font = pygame.font.SysFont(None, self.FONT_SIZE)


    # Function to render HUD (page number, etc.)
    def _prepare_surface(self, display_name, display_page, display_page_count):
        next_page = None
        if display_page > 1:
            next_page = display_page + 1
            if next_page > display_page_count:
                next_page = None
        if next_page is not None:
            text = f"{display_name} — Page {display_page}, {display_page + 1} of {display_page_count}"
        else:
            text = f"{display_name} — Page {display_page} of {display_page_count}"
        text_surface = self.font.render(text, True, (255, 255, 255))

        # Apply transparency to text
        text_surface.set_alpha(self.hud_alpha)

        # Get text size
        text_rect = text_surface.get_rect()

        # Define the rectangle for the HUD
        self.hud_width = text_rect.width + self.PADDING * 2
        self.height = text_rect.height + self.PADDING

        # Draw the rounded rectangle
        self.surface = pygame.Surface((self.hud_width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.surface, (0, 0, 0, 255), (0, 0, self.hud_width, self.height), border_radius=self.RADIUS)

        # Render the text on top of the rectangle
        self.surface.blit(text_surface, (self.PADDING, self.PADDING // 2))


    def show(self, display_name, display_page, display_page_count):
        self.timer = time.time() # Reset HUD visibility
        self.hud_alpha = 255         # Reset alpha to full opacity
        self._prepare_surface(display_name, display_page, display_page_count)
        self.dirty = True


    def handle(self):
        if self.hud_alpha > 0:   # Handle fade-out timing.
            elapsed_time = time.time() - self.timer
            if elapsed_time > self.DISPLAY_TIME:
                if elapsed_time - self.DISPLAY_TIME < self.FADE_TIME:
                    self.hud_alpha = int(255 * (1 - (elapsed_time - self.DISPLAY_TIME) / self.FADE_TIME))
                    self.dirty = True
                else:
                    if self.hud_alpha != 0:
                        self.dirty = True
                    self.hud_alpha = 0  # Fully faded out
        return self.dirty


    def render(self, screen, screen_width, screen_height):
        if self.hud_alpha > 0:
            x = (screen_width - self.hud_width) // 2
            y = screen_height - self.height - self.Y_OFFSET  # Centered near bottom
            self.surface.set_alpha(self.hud_alpha)
            screen.blit(self.surface, (x, y))
        self.dirty = False




