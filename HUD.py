import pygame
import time
from typing import Optional

# Navigation HUD settings
HUD_DISPLAY_TIME = 3    # HUD fully visible for 3 seconds
HUD_FADE_TIME = 1       # 1 second to fade out
HUD_RADIUS = 11         # Your preferred radius
HUD_FONT_SIZE = 28      # Your preferred font size
HUD_Y_OFFSET = 8        # Your preferred offset from the bottom
HUD_PADDING = 20        # Padding inside HUD

hud_surface: Optional[pygame.Surface] = None
hud_width = 0
hud_height = 0
hud_timer:float = 0
hud_alpha = 0
hud_dirty = False
hud_font: Optional[pygame.font.Font] = None


# Function to render HUD (page number, etc.)
def _render_hud(display_name, display_page, display_page_count):
    global hud_surface
    global hud_width
    global hud_height
    global hud_font
    next_page = None
    if display_page > 1:
        next_page = display_page + 1
        if next_page > display_page_count:
            next_page = None
    if next_page is not None:
        text = f"{display_name} — Page {display_page}, {display_page + 1} of {display_page_count}"
    else:
        text = f"{display_name} — Page {display_page} of {display_page_count}"
    text_surface = hud_font.render(text, True, (255, 255, 255))

    # Apply transparency to text
    text_surface.set_alpha(hud_alpha)

    # Get text size
    text_rect = text_surface.get_rect()

    # Define the rectangle for the HUD
    hud_width = text_rect.width + HUD_PADDING * 2
    hud_height = text_rect.height + HUD_PADDING

    # Draw the rounded rectangle
    hud_surface = pygame.Surface((hud_width, hud_height), pygame.SRCALPHA)
    pygame.draw.rect(hud_surface, (0, 0, 0, 255), (0, 0, hud_width, hud_height), border_radius=HUD_RADIUS)

    # Render the text on top of the rectangle
    hud_surface.blit(text_surface, (HUD_PADDING, HUD_PADDING // 2))


def show_HUD(display_name, display_page, display_page_count):
    global hud_timer
    global hud_alpha
    global hud_dirty

    hud_timer = time.time() # Reset HUD visibility
    hud_alpha = 255         # Reset alpha to full opacity
    _render_hud(display_name, display_page, display_page_count)
    hud_dirty = True


def handle_HUD():
    global hud_timer
    global hud_alpha
    global hud_dirty
    if hud_alpha > 0:   # Handle fade-out timing.
        elapsed_time = time.time() - hud_timer
        if elapsed_time > HUD_DISPLAY_TIME:
            if elapsed_time - HUD_DISPLAY_TIME < HUD_FADE_TIME:
                hud_alpha = int(255 * (1 - (elapsed_time - HUD_DISPLAY_TIME) / HUD_FADE_TIME))
                hud_dirty = True
            else:
                if hud_alpha != 0:
                    hud_dirty = True
                hud_alpha = 0  # Fully faded out
    return hud_dirty


def render_HUD(screen, screen_width, screen_height):
    global hud_surface
    global hud_alpha
    global hud_dirty
    if hud_alpha > 0:
        x = (screen_width - hud_width) // 2
        y = screen_height - hud_height - HUD_Y_OFFSET  # Centered near bottom
        hud_surface.set_alpha(hud_alpha)
        screen.blit(hud_surface, (x, y))
    hud_dirty = False


def init_HUD():
    global hud_font
    hud_font = pygame.font.SysFont(None, HUD_FONT_SIZE)

