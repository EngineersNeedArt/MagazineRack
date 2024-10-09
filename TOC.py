import os
import pygame
import time


# TOC HUD settings
TOC_FADE_TIME = 1  # 1 second to fade out
TOC_RADIUS = 7  # Preferred radius
TOC_STROKE = 3  # Stroke thickness
TOC_FONT_SIZE = 28  # Your preferred font size
TOC_MARGIN = 8  # Padding inside TOC
COLUMN_H_PADDING = 8  # Padding between columns

directory_path = None
base_directories = []
base_files = []

toc_visible = False
toc_alpha = 0
toc_dirty = False
toc_timer = None
toc_x = 0
toc_y = 0
toc_wide = 0
toc_tall = 0
toc_surface = None
toc_column_1 = pygame.Rect(0, 0, 0, 0)
toc_column_2 = pygame.Rect(0, 0, 0, 0)
toc_column_3 = pygame.Rect(0, 0, 0, 0)
toc_column_4 = pygame.Rect(0, 0, 0, 0)


def _update_toc_surface():
    global toc_wide
    global toc_tall
    global toc_surface
    global toc_surface
    global base_directories
    global toc_column_1

    # Define colors
    WHITE = (255, 255, 255)
    BLACK_TRANSPARENT = (0, 0, 0, 128)  # Black with 50% alpha

    # Draw the rounded rectangle
    pygame.draw.rect(toc_surface, WHITE, (0, 0, toc_wide, toc_tall), border_radius=TOC_RADIUS)
    pygame.draw.rect(toc_surface, BLACK_TRANSPARENT,
                     (TOC_STROKE, TOC_STROKE, toc_wide - (TOC_STROKE * 2), toc_tall - (TOC_STROKE * 2)),
                     border_radius=TOC_RADIUS - TOC_STROKE)

    font = pygame.font.SysFont(None, TOC_FONT_SIZE)
    text_x = toc_column_1.left
    text_y = toc_column_1.top
    for item in base_directories:
        text_surface = font.render(item, True, WHITE)
        toc_surface.blit(text_surface, (text_x, text_y))
        text_y = text_y + TOC_FONT_SIZE


def init_TOC(base_path, screen_wide, screen_tall):
    global directory_path
    global base_directories
    global base_files
    global toc_x
    global toc_y
    global toc_wide
    global toc_tall
    global toc_surface
    global toc_column_1
    global toc_column_2
    global toc_column_3
    global toc_column_4

    directory_path = base_path

    toc_x = 10  # X position
    toc_y = 10  # Y position
    toc_wide = screen_wide - 20  # Width
    toc_tall = screen_tall - 20  # Height
    toc_surface = pygame.Surface((toc_wide, toc_tall), pygame.SRCALPHA)

    column_wide = (toc_wide - ((TOC_MARGIN * 2) + (COLUMN_H_PADDING * 3))) // 4
    column_tall = toc_tall - (TOC_MARGIN * 2)
    toc_column_1 = pygame.Rect(TOC_MARGIN, TOC_MARGIN, column_wide, column_tall)
    toc_column_2 = pygame.Rect(TOC_MARGIN + column_wide + COLUMN_H_PADDING, TOC_MARGIN, column_wide, column_tall)
    toc_column_3 = pygame.Rect(TOC_MARGIN + column_wide + (COLUMN_H_PADDING * 2), TOC_MARGIN, column_wide, column_tall)
    toc_column_4 = pygame.Rect(TOC_MARGIN + column_wide + (COLUMN_H_PADDING * 3), TOC_MARGIN, column_wide, column_tall)

    # Get a list of file and directory names
    contents = os.listdir(directory_path)

    for item in contents:
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            base_directories.append(item)
        elif item_path.endswith('.pdf'):
            base_files.append(item)


def handle_TOC() -> bool:
    global toc_visible
    global toc_alpha
    global toc_timer
    global toc_dirty

    if (not toc_visible) and (toc_alpha > 0):
        elapsed_time = time.time() - toc_timer  # Handle fade-out timing
        if elapsed_time < TOC_FADE_TIME:
            toc_alpha = int(255 * (TOC_FADE_TIME - elapsed_time))
        else:
            toc_alpha = 0  # Fully faded out
        toc_dirty = True
    return toc_dirty


def render_TOC(screen):
    global toc_dirty
    global toc_alpha
    global toc_x
    global toc_y
    global toc_surface

    if not toc_dirty:
        return

    toc_surface.set_alpha(toc_alpha)
    screen.blit(toc_surface, (toc_x, toc_y))
    toc_dirty = False


def is_TOC_visible()->bool:
    global toc_visible
    return toc_visible


def toggle_TOC(screen):
    global toc_visible
    global toc_alpha
    global toc_timer
    global toc_dirty

    toc_visible = not toc_visible
    if toc_visible:
        _update_toc_surface()
        toc_alpha = 255
    else:
        toc_timer = time.time()  # Reset HUD visibility
    toc_dirty = True
