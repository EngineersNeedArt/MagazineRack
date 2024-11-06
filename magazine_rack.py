import os
import pygame
import sys
from hud import HUD
from magazine import Magazine
from prefs import Prefs
from sound_effects import SoundEffects
from toc import TOC
from toc_data import TOCData


# DEBUG flag
DEBUG = False  # Is not FULLSCREEN in Debug mode.


class MagazineRack:

    def __init__(self, base_path):
        pygame.init()
        if DEBUG:
            self.screen = pygame.display.set_mode((1024, 768))
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Magazine Rack")
        self.prefs = Prefs("config.json")
        self.progress_dict = self.prefs.get("magazine_progress_dict") or {}
        self.bookmarks_dict = self.prefs.get("magazine_bookmarks_dict") or {}
        self.sound_effects = SoundEffects()
        self.screen_width, self.screen_height = self.screen.get_size()
        self.max_width = self.screen_width // 2
        self.max_height = self.screen_height
        self.hud = HUD()
        self.toc_data = TOCData(base_path, self.prefs.get("last_magazine_path"))
        self.toc = TOC(self.screen_width, self.screen_height, self.progress_dict, self.bookmarks_dict)
        self.base_path = base_path
        self.is_running = True
        self.magazine_key = ""
        self.page_progress = 0
        self.display_name = ""
        self.dirty = False
        self.magazine = None
        self.load_magazine (self.prefs.get("last_magazine_path"), self.prefs.get("last_page_index"))
        self.bookmark_left_image = pygame.transform.smoothscale(pygame.image.load('graphics/bookmark_left.png'), (38, 64))
        self.bookmark_left_image = self.bookmark_left_image.convert_alpha()
        self.bookmark_right_image = pygame.transform.smoothscale(pygame.image.load('graphics/bookmark_right.png'), (38, 64))
        self.bookmark_right_image = self.bookmark_right_image.convert_alpha()


    def _store_page_progress(self):
        current_page = self.magazine.current_page
        self.prefs.set("last_page_index", current_page)
        if (self.page_progress > 0) and (current_page > self.page_progress):
            self.page_progress = current_page
            percent = (self.page_progress * 100) // self.magazine.page_count
            # Special case when the magazine is complete, store 0 (zero).
            if self.magazine.is_last_page():
                self.page_progress = 0
                percent = 100
            magazine_dict = self.progress_dict.get(self.magazine_key) or {}
            magazine_dict["page_progress"] = self.page_progress
            magazine_dict["percent_progress"] = percent
            self.progress_dict[self.magazine_key] = magazine_dict
            self.prefs.set("magazine_progress_dict", self.progress_dict)


    def _get_page_and_facing_page_indices(self):
        page_index = 0
        facing_index = None
        current_page = self.magazine.current_page
        if current_page > 1:
            left_page_number = current_page if current_page % 2 == 0 else current_page - 1
            right_page_number = left_page_number + 1
            if right_page_number > self.magazine.page_count:
                right_page_number = None
            page_index = left_page_number - 1
            facing_index = right_page_number - 1 if right_page_number else None
        return page_index, facing_index


    def _handle_left_key(self):
        self.dirty = False
        if self.toc.visible:
            self.sound_effects.play_nav_left()
            self.dirty = self.toc_data.go_left()
            if self.dirty:
                self.toc.update(self.toc_data)
        else:
            if self.magazine:
                self.dirty = self.magazine.go_prev_page()
                if self.dirty:
                    self._store_page_progress()
                    self.hud.show(self.display_name, self.magazine.current_page, self.magazine.page_count)
                    self.sound_effects.play_left_page()
                else:
                    self.sound_effects.play_fail()
        return self.dirty


    def _handle_right_key(self):
        self.dirty = False
        if self.toc.visible:
            self.sound_effects.play_nav_right()
            self.dirty = self.toc_data.go_right()
            if self.dirty:
                self.toc.update(self.toc_data)
        else:
            if self.magazine:
                self.dirty = self.magazine.go_next_page()
                if self.dirty:
                    self._store_page_progress()
                    self.hud.show(self.display_name, self.magazine.current_page, self.magazine.page_count)
                    self.sound_effects.play_right_page()
                else:
                    self.sound_effects.play_fail()
        return self.dirty


    def _handle_up_key(self):
        if self.toc.visible:
            self.sound_effects.play_nav_up()
            self.dirty = self.toc_data.go_up()
            if self.dirty:
                self.toc.update(self.toc_data)


    def _handle_down_key(self):
        if self.toc.visible:
            self.sound_effects.play_nav_down()
            self.dirty = self.toc_data.go_down()
            if self.dirty:
                self.toc.update(self.toc_data)


    def _handle_enter_key(self):
        if self.toc.visible:
            path = self.toc_data.selected_path
            if (path is None) or (TOCData.is_directory(path)):
                self.sound_effects.play_fail()
            else:
                self.sound_effects.play_open_magazine()
                self.toc.hide()
                self.load_magazine(path, None)
        else:
            self._cycle_bookmark()
            self.dirty = True


    def _handle_toc_toggle_key(self):
        if self.magazine:
            if self.toc.toggle(self.toc_data):
                self.sound_effects.play_open_toc()
            else:
                self.sound_effects.play_close_toc()
        else:
            self.sound_effects.play_fail()


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
                    self._handle_toc_toggle_key()
                elif event.key == pygame.K_RETURN:
                    self._handle_enter_key()
            elif event.type == pygame.QUIT:
                self.is_running = False


    def _is_page_bookmarked(self, page_index)->bool:
        return str(page_index) in self.magazine_bookmarks


    def _set_bookmark(self, page_index: int) -> None:
        self.magazine_bookmarks[str(page_index)] = True


    def _clear_bookmark(self, page_index: int) -> None:
        self.magazine_bookmarks.pop(str(page_index), None)


    def _cycle_bookmark(self):
        (page_index, facing_index) = self._get_page_and_facing_page_indices()
        if facing_index is None:
            bookmarked = self._is_page_bookmarked(page_index)
            if bookmarked:
                self._clear_bookmark(page_index)
                self.sound_effects.play_bookmark_off()
            else:
                self._set_bookmark(page_index)
                self.sound_effects.play_bookmark_on()
        else:
            page_bookmarked = self._is_page_bookmarked(page_index)
            facing_bookmarked = self._is_page_bookmarked(facing_index)
            if page_bookmarked:
                if not facing_bookmarked:
                    self._clear_bookmark(page_index)
                    self._set_bookmark(facing_index)
                    self.sound_effects.play_bookmark_on()
                else:
                    self._clear_bookmark(page_index)
                    self._clear_bookmark(facing_index)
                    self.sound_effects.play_bookmark_off()
            else:
                if not facing_bookmarked:
                    self._set_bookmark(page_index)
                    self.sound_effects.play_bookmark_on()
                else:
                    self._set_bookmark(page_index)
                    self.sound_effects.play_bookmark_on()
        self.bookmarks_dict[self.magazine_key] = self.magazine_bookmarks
        self.prefs.set("magazine_bookmarks_dict", self.bookmarks_dict)


    def _displayBookmark(self, surface, onLeft):
        if onLeft:
            surface.blit(self.bookmark_left_image, (0, 0))
        else:
            surface.blit(self.bookmark_right_image, (surface.get_width() - self.bookmark_right_image.get_width(), 0))


    # Center the image
    def _display_page_centered(self, page_index)->bool:
        img = self.magazine.image_for_page(page_index, self.max_width, self.max_height)
        if not img:
            return False
        img_width, img_height = img.size
        mode = img.mode
        data = img.tobytes()
        pygame_image = pygame.image.fromstring(data, (img_width, img_height), mode)
        if self._is_page_bookmarked(page_index):
            self._displayBookmark(pygame_image, True)
        x_pos = (self.screen_width - img_width) // 2
        y_pos = (self.screen_height - img_height) // 2
        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame_image, (x_pos, y_pos))
        return True


    # Display two-up.
    def _display_pages_two_up(self, left_index, right_index):
        self.screen.fill((0, 0, 0))

        if left_index:
            left_img = self.magazine.image_for_page(left_index, self.max_width, self.max_height)
            if not left_img:
                return False
            mode_left = left_img.mode
            size_left = left_img.size
            data_left = left_img.tobytes()
            pygame_left_image = pygame.image.fromstring(data_left, size_left, mode_left)
            left_x = (self.screen_width // 2 - size_left[0]) - 1
            center_y = (self.screen_height - size_left[1]) // 2
            if self._is_page_bookmarked(left_index):
                self._displayBookmark(pygame_left_image, True)
            self.screen.blit(pygame_left_image, (left_x, center_y))

        if right_index:
            right_img = self.magazine.image_for_page(right_index, self.max_width, self.max_height)
            if not right_img:
                return False
            mode_right = right_img.mode
            size_right = right_img.size
            data_right = right_img.tobytes()
            pygame_right_image = pygame.image.fromstring(data_right, size_right, mode_right)
            right_x = (self.screen_width // 2) + 1
            center_y = (self.screen_height - size_right[1]) // 2
            if self._is_page_bookmarked(right_index):
                self._displayBookmark(pygame_right_image, False)
            self.screen.blit(pygame_right_image, (right_x, center_y))
        return True


    def _render_magazine_spread(self)->bool:
        if self.magazine:
            (page_index, facing_index) = self._get_page_and_facing_page_indices()
            if facing_index is None:
                return self._display_page_centered(page_index)
            else:
                return self._display_pages_two_up(page_index, facing_index)


    def _update_screen(self):
        if self.toc_dirty or self.hud_dirty or self.dirty:  # Only render when needed
            self.dirty = self._render_magazine_spread() == False
            if self.hud._visible:
                self.hud.render(self.screen)
            if self.toc.visible:
                self.toc.render(self.screen)
            pygame.display.flip()


    def load_magazine(self, path, initial_page):
        if path:
            # Get the 'page_progress' from our prefs, the user may have already read part of this magazine.
            self.magazine_key = os.path.basename(path)
            magazine_dict = self.progress_dict.get(self.magazine_key) or {}
            self.page_progress = magazine_dict.get("page_progress")
            if self.page_progress is None:
                self.page_progress = 1

            self.magazine_bookmarks = self.bookmarks_dict.get(self.magazine_key) or {}

            # If no 'initial_page' was specified, defer to the 'page_progress' page.
            # A 'page_progress' of 0 (zero) is a special case indicating the magazine was completed, start at beginning again.
            if (self.page_progress) and (not initial_page):
                if self.page_progress != 0:
                    initial_page = self.page_progress
                else:
                    initial_page = 1
            self.magazine = Magazine(path, initial_page)
            if self.magazine:
                self.prefs.set("last_magazine_path", path)
                self.display_name = self.magazine_key[:-4]  # Removes the last 4 characters ('.pdf')
                current_page = self.magazine.current_page
                self.dirty = True
                self.hud.show(self.display_name, current_page, self.magazine.page_count)


    def run(self):
        if not self.magazine:
            self.toc.show(self.toc_data)
        while self.is_running:
            self._handle_events()
            self.toc_dirty = self.toc.handle()
            self.hud_dirty = self.hud.handle()
            self._update_screen()
            pygame.time.delay(100)


if __name__ == "__main__":
    app = MagazineRack('content')
    app.run()
    pygame.quit()
    sys.exit()