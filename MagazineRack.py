import os
import pygame
from PIL import Image
from typing import Optional
from hud import HUD
from magazine import Magazine
from Sounds import *
from toc import TOC
from toc_data import TOC_Data

# DEBUG flag
DEBUG = True  # Is not FULLSCREEN in Debug mode.


display_name = 'popsci'
dirty = False  # Track when rendering is needed


def load_magazine(path):
    global display_name
    global dirty
    if path is None:
        return
    magazine = Magazine(path)
    document = magazine.get_document()
    display_name = os.path.basename(path)
    display_name = display_name[:-4]  # Removes the last 4 characters ('.pdf')
    current_page = magazine.get_current_page()
    display_pdf_pages_two_up(path, current_page, magazine)
    dirty = True
    hud.show(display_name, current_page, magazine.get_page_count())


def display_pdf_pages_two_up(pdf_path, initial_page_number, magazine):
    global screen
    global screen_width
    global screen_height
    global dirty

    # Center the image
    def display_page_centered(page_index, screen, magazine):
        img = magazine.image_for_page(page_index, max_width, max_height)
        img_width, img_height = img.size
        mode = img.mode
        data = img.tobytes()
        pygame_image = pygame.image.fromstring(data, (img_width, img_height), mode)
        x_pos = (screen_width - img_width) // 2
        y_pos = (screen_height - img_height) // 2
        screen.fill((0, 0, 0))
        screen.blit(pygame_image, (x_pos, y_pos))
        
    # Display two-up.
    def display_pages_two_up(left_index, right_index, screen, magazine):
        left_img = magazine.image_for_page(left_index, max_width, max_height)
        right_img = magazine.image_for_page(right_index, max_width, max_height)

        mode_left = left_img.mode
        size_left = left_img.size
        data_left = left_img.tobytes()
        pygame_left_image = pygame.image.fromstring(data_left, size_left, mode_left)

        mode_right = right_img.mode
        size_right = right_img.size
        data_right = right_img.tobytes()
        pygame_right_image = pygame.image.fromstring(data_right, size_right, mode_right)

        left_x = (screen_width // 2 - size_left[0]) - 1
        right_x = (screen_width // 2) + 1
        center_y = (screen_height - size_left[1]) // 2

        screen.fill((0, 0, 0))
        screen.blit(pygame_left_image, (left_x, center_y))
        screen.blit(pygame_right_image, (right_x, center_y))


    def handle_left_key(magazine):
        global display_name
        global dirty
        dirty = False
        if toc.is_visible():
            dirty = toc_data_source.left_TOC_event()
            if dirty:
                toc.update(toc_data_source)
        else:
            dirty = magazine.go_prev_page()
            if dirty:
                hud.show(display_name, magazine.get_current_page(), magazine.get_page_count())
                play_right_sound()
            else:
                play_fail_sound()
        return dirty

    def handle_right_key(magazine):
        global display_name
        global dirty
        dirty = False
        if toc.is_visible():
            dirty = toc_data_source.right_TOC_event()
            if dirty:
                toc.update(toc_data_source)
        else:
            dirty = magazine.go_next_page()
            if dirty:
                hud.show(display_name, magazine.get_current_page(), magazine.get_page_count())
                play_right_sound()
            else:
                play_fail_sound()
        return dirty

    def handle_up_key():
        global dirty
        if toc.is_visible():
            dirty = toc_data_source.up_TOC_event()
            if dirty:
                toc.update(toc_data_source)

    def handle_down_key():
        global dirty
        if toc.is_visible():
            dirty = toc_data_source.down_TOC_event()
            if dirty:
                toc.update(toc_data_source)

    def handle_enter_key():
        global display_name
        global dirty
        if toc.is_visible():
            dirty = toc.activate(toc_data_source)
            if dirty:
                path = toc_data_source.selected_path()
                load_magazine(path)


    # Function to render the current page
    def render_magazine_spread(current_page):
        if current_page == 1:
            display_page_centered(0, screen, magazine)
        elif current_page > 1:
            left_page_number = current_page if current_page % 2 == 0 else current_page - 1
            right_page_number = left_page_number + 1
            if right_page_number > magazine.get_page_count():
                right_page_number = None
            left_page = left_page_number - 1
            right_page = right_page_number - 1 if right_page_number else None
            display_pages_two_up(left_page, right_page, screen, magazine)


    running = True
    while running:
        toc_dirty = toc.handle()
        hud_dirty = hud.handle()
        if toc_dirty or hud_dirty or dirty:  # Only render when needed
            current_page = magazine.get_current_page()
            render_magazine_spread(current_page)
            if hud_dirty:
                hud.render(screen, screen_width, screen_height)
            if toc_dirty:
                toc.render(screen)
            pygame.display.flip()
            dirty = False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dirty = handle_left_key(magazine)
                elif event.key == pygame.K_RIGHT:
                    dirty = handle_right_key(magazine)
                elif event.key == pygame.K_UP:
                    handle_up_key()
                elif event.key == pygame.K_DOWN:
                    handle_down_key()
                elif event.key == pygame.K_SPACE:
                    toc.toggle(toc_data_source)
                elif event.key == pygame.K_RETURN:
                    handle_enter_key()
            elif event.type == pygame.QUIT:
                running = False

    pygame.quit()


# Example usage
pygame.init()
pygame.key.set_repeat(1000, 200)

if DEBUG:
    screen = pygame.display.set_mode((1024, 768))
else:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
max_width = screen_width // 2
max_height = screen_height
pygame.display.set_caption("Magazine Rack")

hud = HUD ()
toc_data_source = TOC_Data ('content')
toc = TOC(screen_width, screen_height)

path = "content/Popular Science/1960\'s/Popular Science 1963/1963-08 Popular Science.pdf"
load_magazine(path)
