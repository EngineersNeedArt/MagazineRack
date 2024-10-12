import pygame
from PIL import Image
from Pages import *
import time
from Magazine import *
from Sounds import *
from TOC import *
from TOC_Data import *

# DEBUG flag
DEBUG = True  # Is not FULLSCREEN in Debug mode.


current_page = 0


def load_magazine(path):
    global current_page

    if path is None:
            return

    document = init_magazine(path)
    current_page = 1
    set_pdf_document(document)
#   display_name = "Popular Science (Aug 1963)"
    display_pdf_pages_two_up(path, current_page)


def display_pdf_pages_two_up(pdf_path, initial_page_number):
    global screen
    global screen_width
    global screen_height

    # Navigation HUD settings
    NAV_HUD_DISPLAY_TIME = 3  # HUD fully visible for 3 seconds
    NAV_HUD_FADE_TIME = 1  # 1 second to fade out
    NAV_HUD_RADIUS = 11  # Your preferred radius
    NAV_FONT_SIZE = 28  # Your preferred font size
    NAV_HUD_Y_OFFSET = 8  # Your preferred offset from the bottom
    NAV_HUD_PADDING = 20  # Padding inside HUD

    # Center the image
    def display_page_centered(page_index, screen):
        img = render_page_to_image(page_index, max_width, max_height)
        img_width, img_height = img.size
        mode = img.mode
        data = img.tobytes()
        pygame_image = pygame.image.fromstring(data, (img_width, img_height), mode)
        x_pos = (screen_width - img_width) // 2
        y_pos = (screen_height - img_height) // 2
        screen.fill((0, 0, 0))
        screen.blit(pygame_image, (x_pos, y_pos))
        
    # Display two-up.
    def display_pages_two_up(left_index, right_index, screen):
        left_img = render_page_to_image(left_index, max_width, max_height)
        right_img = render_page_to_image(right_index, max_width, max_height)

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

    # Function to render HUD (page number, etc.)
    def render_nav_hud(current_page, total_pages, alpha):
        font = pygame.font.SysFont(None, NAV_FONT_SIZE)
        next_page = None
        if current_page > 1:
            next_page = current_page + 1
            if next_page > total_pages:
                next_page = None
        if next_page is not None:
            text = f"{display_name} — Page {current_page}, {current_page + 1} of {total_pages}"
        else:
            text = f"{display_name} — Page {current_page} of {total_pages}"
        text_surface = font.render(text, True, (255, 255, 255))

        # Apply transparency to text
        text_surface.set_alpha(alpha)

        # Get text size
        text_rect = text_surface.get_rect()

        # Define the rectangle for the HUD
        hud_width = text_rect.width + NAV_HUD_PADDING * 2
        hud_height = text_rect.height + NAV_HUD_PADDING
        hud_x = (screen_width - hud_width) // 2
        hud_y = screen_height - hud_height - NAV_HUD_Y_OFFSET  # Centered near bottom

        # Draw the rounded rectangle
        rect_surface = pygame.Surface((hud_width, hud_height), pygame.SRCALPHA)
        pygame.draw.rect(rect_surface, (0, 0, 0, alpha / 2), (0, 0, hud_width, hud_height), border_radius=NAV_HUD_RADIUS)
        screen.blit(rect_surface, (hud_x, hud_y))

        # Render the text on top of the rectangle
        screen.blit(text_surface, (hud_x + NAV_HUD_PADDING, hud_y + NAV_HUD_PADDING // 2))


    def handle_left_key():
        dirty = False
        if is_TOC_visible():
            dirty = left_TOC_event()
            if dirty:
                update_TOC()
        else:
            dirty = left_magazine_event()
            if dirty:
                #                           hud_timer = time.time()  # Reset HUD visibility
                #                           hud_alpha = 255  # Reset alpha to full opacity
                play_right_sound()
            else:
                play_fail_sound()
        return dirty

    def handle_right_key():
        dirty = False
        if is_TOC_visible():
            dirty = right_TOC_event()
            if dirty:
                update_TOC()
        else:
            dirty = right_magazine_event()
            if dirty:
                #                           hud_timer = time.time()  # Reset HUD visibility
                #                           hud_alpha = 255  # Reset alpha to full opacity
                play_right_sound()
            else:
                play_fail_sound()
        return dirty

    def handle_up_key():
        if is_TOC_visible():
            dirty = up_TOC_event()
            if dirty:
                update_TOC()

    def handle_down_key():
        if is_TOC_visible():
            dirty = down_TOC_event()
            if dirty:
                update_TOC()

    def handle_enter_key():
        if is_TOC_visible():
            dirty = activate_TOC()
            if dirty:
                path = selected_TOC_path()
                load_magazine(path)

    # Function to render the current page
    def render_magazine_spread(current_page):
        if current_page == 1:
            display_page_centered(0, screen)
        elif current_page > 1:
            left_page_number = current_page if current_page % 2 == 0 else current_page - 1
            right_page_number = left_page_number + 1
            if right_page_number > get_magazine_page_count():
                right_page_number = None
            left_page = left_page_number - 1
            right_page = right_page_number - 1 if right_page_number else None
            display_pages_two_up(left_page, right_page, screen)

    dirty = True  # Track when rendering is needed
    hud_alpha = 255
    hud_timer = time.time()  # Track HUD visibility time

    # Set key repeat with a delay of 200ms and repeat interval of 50ms
    pygame.key.set_repeat(1000, 200)

    running = True
    while running:
        toc_dirty = handle_TOC()
        if toc_dirty or dirty:  # Only render when needed
            current_page = get_current_magazine_page()
            render_magazine_spread(current_page)
#            if hud_alpha > 0:
#                render_nav_hud(current_page, get_magazine_page_count(), hud_alpha)
            render_TOC(screen)
            pygame.display.flip()
            dirty = False

        # Handle fade-out timing
#        elapsed_time = time.time() - hud_timer
#        if elapsed_time > NAV_HUD_DISPLAY_TIME:
#            if elapsed_time - NAV_HUD_DISPLAY_TIME < NAV_HUD_FADE_TIME:
#                hud_alpha = int(255 * (1 - (elapsed_time - NAV_HUD_DISPLAY_TIME) / NAV_HUD_FADE_TIME))
#                dirty = True
#            else:
#                if hud_alpha != 0:
#                    dirty = True
#                hud_alpha = 0  # Fully faded out

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dirty = handle_left_key()
                elif event.key == pygame.K_RIGHT:
                    dirty = handle_right_key()
                elif event.key == pygame.K_UP:
                    handle_up_key()
                elif event.key == pygame.K_DOWN:
                    handle_down_key()
                elif event.key == pygame.K_SPACE:
                    toggle_TOC(screen)
                elif event.key == pygame.K_RETURN:
                    handle_enter_key()

            elif event.type == pygame.QUIT:
                running = False

    pygame.quit()


# Example usage
pygame.init()
#    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
if DEBUG:
    screen = pygame.display.set_mode((1024, 768))
else:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
max_width = screen_width // 2
max_height = screen_height
pygame.display.set_caption("Magazine Rack")

init_TOC_Data ('content')
init_TOC(screen_width, screen_height)

path = "content/Popular Science/1960\'s/Popular Science 1963/1963-08 Popular Science.pdf"
load_magazine(path)