import os
import pygame
import sys
from hud import HUD
from magazine import Magazine
from sound_effects import SoundEffects
from toc import TOC
from toc_data import TOC_Data


# DEBUG flag
DEBUG = False  # Is not FULLSCREEN in Debug mode.


class MagazineRack:

    def __init__(self, base_path):
        pygame.init()
        pygame.key.set_repeat(1000, 200)
        if DEBUG:
            self.screen = pygame.display.set_mode((1024, 768))
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Magazine Rack")
        self.sound_effects = SoundEffects()
        self.screen_width, self.screen_height = self.screen.get_size()
        self.max_width = self.screen_width // 2
        self.max_height = self.screen_height
        self.hud = HUD()
        self.toc_data = TOC_Data(base_path)
        self.toc = TOC(self.screen_width, self.screen_height)
        self.base_path = base_path
        self.is_running = True
        self.dirty = False
        self.magazine = None


    def _handle_left_key(self):
        self.dirty = False
        if self.toc.is_visible():
            self.dirty = self.toc_data.go_left()
            if self.dirty:
                self.toc.update(self.toc_data)
        else:
            self.dirty = self.magazine.go_prev_page()
            if self.dirty:
                self.hud.show(self.display_name, self.magazine.get_current_page(), self.magazine.get_page_count())
                self.sound_effects.play_left()
            else:
                self.sound_effects.play_fail()
        return self.dirty


    def _handle_right_key(self):
        self.dirty = False
        if self.toc.is_visible():
            self.dirty = self.toc_data.go_right()
            if self.dirty:
                self.toc.update(self.toc_data)
        else:
            self.dirty = self.magazine.go_next_page()
            if self.dirty:
                self.hud.show(self.display_name, self.magazine.get_current_page(), self.magazine.get_page_count())
                self.sound_effects.play_right()
            else:
                self.sound_effects.play_fail()
        return self.dirty


    def _handle_up_key(self):
        if self.toc.is_visible():
            self.dirty = self.toc_data.go_up()
            if self.dirty:
                self.toc.update(self.toc_data)


    def _handle_down_key(self):
        if self.toc.is_visible():
            self.dirty = self.toc_data.go_down()
            if self.dirty:
                self.toc.update(self.toc_data)


    def _handle_enter_key(self):
        if self.toc.is_visible():
            self.toc.hide()
            path = self.toc_data.selected_path()
            self.load_magazine(path)


    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
                elif event.key == pygame.K_LEFT:
                    self.dirty = self._handle_left_key()
                elif event.key == pygame.K_RIGHT:
                    self.dirty = self._handle_right_key()
                elif event.key == pygame.K_UP:
                    self._handle_up_key()
                elif event.key == pygame.K_DOWN:
                    self._handle_down_key()
                elif event.key == pygame.K_SPACE:
                    self.toc.toggle(self.toc_data)
                elif event.key == pygame.K_RETURN:
                    self._handle_enter_key()
            elif event.type == pygame.QUIT:
                self.is_running = False


    # Center the image
    def _display_page_centered(self, page_index):
        img = self.magazine.image_for_page(page_index, self.max_width, self.max_height)
        img_width, img_height = img.size
        mode = img.mode
        data = img.tobytes()
        pygame_image = pygame.image.fromstring(data, (img_width, img_height), mode)
        x_pos = (self.screen_width - img_width) // 2
        y_pos = (self.screen_height - img_height) // 2
        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame_image, (x_pos, y_pos))


    # Display two-up.
    def _display_pages_two_up(self, left_index, right_index):
        left_img = self.magazine.image_for_page(left_index, self.max_width, self.max_height)
        right_img = self.magazine.image_for_page(right_index, self.max_width, self.max_height)

        mode_left = left_img.mode
        size_left = left_img.size
        data_left = left_img.tobytes()
        pygame_left_image = pygame.image.fromstring(data_left, size_left, mode_left)

        mode_right = right_img.mode
        size_right = right_img.size
        data_right = right_img.tobytes()
        pygame_right_image = pygame.image.fromstring(data_right, size_right, mode_right)

        left_x = (self.screen_width // 2 - size_left[0]) - 1
        right_x = (self.screen_width // 2) + 1
        center_y = (self.screen_height - size_left[1]) // 2

        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame_left_image, (left_x, center_y))
        self.screen.blit(pygame_right_image, (right_x, center_y))


    def _render_magazine_spread(self):
        if self.magazine:
            current_page = self.magazine.get_current_page()
            if current_page == 1:
                self._display_page_centered(0)
            elif current_page > 1:
                left_page_number = current_page if current_page % 2 == 0 else current_page - 1
                right_page_number = left_page_number + 1
                if right_page_number > self.magazine.get_page_count():
                    right_page_number = None
                left_page = left_page_number - 1
                right_page = right_page_number - 1 if right_page_number else None
                self._display_pages_two_up(left_page, right_page)


    def _update_screen(self):
        if self.toc_dirty or self.hud_dirty or self.dirty:  # Only render when needed
            self._render_magazine_spread()
            if self.hud.is_visible():
                self.hud.render(self.screen)
            if self.toc.is_visible():
                self.toc.render(self.screen)
            pygame.display.flip()
            self.dirty = False


    def load_magazine(self, path):
        if path is None:
            return
        self.magazine = Magazine(path)
        self.display_name = os.path.basename(path)
        self.display_name = self.display_name[:-4]  # Removes the last 4 characters ('.pdf')
        current_page = self.magazine.get_current_page()
        self.dirty = True
        self.hud.show(self.display_name, current_page, self.magazine.get_page_count())


    def run(self):
        self.toc.show(self.toc_data)
        while self.is_running:
            self._handle_events()
            self.toc_dirty = self.toc.handle()
            self.hud_dirty = self.hud.handle()
            self._update_screen()


if __name__ == "__main__":
    app = MagazineRack('content')
    app.run()
    pygame.quit()
    sys.exit()