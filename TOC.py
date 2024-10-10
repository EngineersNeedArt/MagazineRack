import pygame
import time
from typing import Optional
from TOC_Data import *


# TOC HUD settings
TOC_FADE_TIME = 1  # 1 second to fade out
TOC_RADIUS = 7  # Preferred radius
TOC_STROKE = 3  # Stroke thickness
TOC_FONT_SIZE = 28  # Your preferred font size
TOC_MARGIN = 8  # Padding inside TOC
COLUMN_H_PADDING = 8  # Padding between columns
TOC_TEXT_X_OFFSET = 3
TOC_TEXT_Y_OFFSET = 5

toc_visible = False
toc_alpha = 0
toc_dirty = False
toc_timer: float = 0
toc_x = 0
toc_y = 0
toc_wide = 0
toc_tall = 0
toc_surface: Optional[pygame.Surface] = None
toc_column_1 = pygame.Rect(0, 0, 0, 0)
toc_column_2 = pygame.Rect(0, 0, 0, 0)
toc_column_3 = pygame.Rect(0, 0, 0, 0)
toc_column_4 = pygame.Rect(0, 0, 0, 0)


def _update_toc_surface():
    global toc_wide
    global toc_tall
    global toc_surface
    global base_directories
    global toc_column_1

    def _draw_row(text_x, text_y, selected, bounds, surface):
        if selected:
            # Make a copy of the original rect
            item_bounds = bounds.copy()
            item_bounds.height = TOC_FONT_SIZE
            item_bounds.y = text_y
            pygame.draw.rect(surface, WHITE, item_bounds)
            text_surface = font.render(item, True, BLACK_TRANSPARENT)
        else:
            text_surface = font.render(item, True, WHITE)
        surface.blit(text_surface, (text_x + TOC_TEXT_X_OFFSET, text_y + TOC_TEXT_Y_OFFSET))

    # Define colors
    WHITE = (255, 255, 255)
    BLACK_TRANSPARENT = (0, 0, 0, 128)  # Black with 50% alpha

    # Draw the rounded rectangle
    pygame.draw.rect(toc_surface, WHITE, (0, 0, toc_wide, toc_tall), border_radius=TOC_RADIUS)
    pygame.draw.rect(toc_surface, BLACK_TRANSPARENT,
                     (TOC_STROKE, TOC_STROKE, toc_wide - (TOC_STROKE * 2), toc_tall - (TOC_STROKE * 2)),
                     border_radius=TOC_RADIUS - TOC_STROKE)

    font = pygame.font.SysFont(None, TOC_FONT_SIZE)

    # Draw column 1.
    directories, files, selected_row = get_TOC_column_1_directories_files()
    text_x = toc_column_1.left
    text_y = toc_column_1.top
    row = 0
    for item in directories:
        _draw_row(text_x, text_y, row == selected_row, toc_column_1, toc_surface)
        text_y = text_y + TOC_FONT_SIZE
        row = row + 1
    for item in files:
        _draw_row(text_x, text_y, row == selected_row, toc_column_1, toc_surface)
        text_y = text_y + TOC_FONT_SIZE
        row = row + 1

    # Draw column 2.
    directories, files, selected_row = get_TOC_column_2_directories_files()
    text_x = toc_column_2.left
    text_y = toc_column_2.top
    row = 0
    for item in directories:
        _draw_row(text_x, text_y, row == selected_row, toc_column_2, toc_surface)
        text_y = text_y + TOC_FONT_SIZE
        row = row + 1
    for item in files:
        _draw_row(text_x, text_y, row == selected_row, toc_column_2, toc_surface)
        text_y = text_y + TOC_FONT_SIZE
        row = row + 1

    # Draw column 3.
    directories, files, selected_row = get_TOC_column_3_directories_files()
    text_x = toc_column_3.left
    text_y = toc_column_3.top
    row = 0
    for item in directories:
        _draw_row(text_x, text_y, row == selected_row, toc_column_3, toc_surface)
        text_y = text_y + TOC_FONT_SIZE
        row = row + 1
    for item in files:
        _draw_row(text_x, text_y, row == selected_row, toc_column_3, toc_surface)
        text_y = text_y + TOC_FONT_SIZE
        row = row + 1

    # Draw column 4.
    directories, files, selected_row = get_TOC_column_4_directories_files()
    text_x = toc_column_4.left
    text_y = toc_column_4.top
    row = 0
    for item in directories:
        _draw_row(text_x, text_y, row == selected_row, toc_column_4, toc_surface)
        text_y = text_y + TOC_FONT_SIZE
        row = row + 1
    for item in files:
        _draw_row(text_x, text_y, row == selected_row, toc_column_4, toc_surface)
        text_y = text_y + TOC_FONT_SIZE
        row = row + 1

def init_TOC(screen_wide, screen_tall):
    global toc_x
    global toc_y
    global toc_wide
    global toc_tall
    global toc_surface
    global toc_column_1
    global toc_column_2
    global toc_column_3
    global toc_column_4

    toc_x = 10  # X position
    toc_y = 10  # Y position
    toc_wide = screen_wide - 20  # Width
    toc_tall = screen_tall - 20  # Height
    toc_surface = pygame.Surface((toc_wide, toc_tall), pygame.SRCALPHA)

    column_wide = (toc_wide - ((TOC_MARGIN * 2) + (COLUMN_H_PADDING * 3))) // 4
    column_tall = toc_tall - (TOC_MARGIN * 2)
    toc_column_1 = pygame.Rect(TOC_MARGIN, TOC_MARGIN, column_wide, column_tall)
    toc_column_2 = pygame.Rect(TOC_MARGIN + column_wide + COLUMN_H_PADDING, TOC_MARGIN, column_wide, column_tall)
    toc_column_3 = pygame.Rect(TOC_MARGIN + (column_wide * 2) + (COLUMN_H_PADDING * 2), TOC_MARGIN, column_wide, column_tall)
    toc_column_4 = pygame.Rect(TOC_MARGIN + (column_wide * 3) + (COLUMN_H_PADDING * 3), TOC_MARGIN, column_wide, column_tall)


def handle_TOC()->bool:
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


def update_TOC():
    global toc_dirty

    _update_toc_surface()
    toc_dirty = True


def activate_TOC():
    global toc_visible
    global toc_timer
    global toc_dirty

    if not toc_visible:
        return False

    toc_visible = False
    toc_timer = time.time()  # Reset HUD visibility
    toc_dirty = True
    if is_TOC_selection_changed():
        return True