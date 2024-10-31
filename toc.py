import pygame
import time


class TOC:
    # TOC HUD settings
    FADE_TIME = 1           # 1 second to fade out
    RADIUS = 7              # Preferred radius
    STROKE = 3              # Stroke thickness
    FONT_SIZE = 22          # Your preferred font size
    CELL_HEIGHT = 28        # Your preferred font size
    MARGIN = 8              # Padding inside TOC
    COLUMN_H_PADDING = 8    # Padding between columns
    TEXT_X_OFFSET = 3
    TEXT_Y_OFFSET = 1

    # Define colors
    WHITE = (255, 255, 255)
    ACTIVE_COLOR = (255, 255, 255)
    INACTIVE_COLOR = (160, 160, 160)
    BLACK_TRANSPARENT = (0, 0, 0, 192)  # Black with 50% alpha

    def __init__(self, screen_wide, screen_tall, progress_data, bookmark_data):
        self.progress_dictionary = progress_data
        self.bookmark_dictionary = bookmark_data
        self._visible = False
        self.alpha = 0
        self.dirty = False
        self.start_time = 0
        self.x_loc = 10  # X position
        self.y_loc = 10  # Y position
        self.width = screen_wide - 20  # Width
        self.toc_tall = screen_tall - 20  # Height
        self.surface = pygame.Surface((self.width, self.toc_tall), pygame.SRCALPHA)
        column_wide = (self.width - ((self.MARGIN * 2) + (self.COLUMN_H_PADDING * 3))) // 4
        column_tall = self.toc_tall - (self.MARGIN * 2)
        self.column_1 = pygame.Rect(self.MARGIN, self.MARGIN, column_wide, column_tall)
        self.column_2 = pygame.Rect(self.MARGIN + column_wide + self.COLUMN_H_PADDING, self.MARGIN, column_wide, column_tall)
        self.column_3 = pygame.Rect(self.MARGIN + (column_wide * 2) + (self.COLUMN_H_PADDING * 2), self.MARGIN, column_wide,
                                   column_tall)
        self.column_4 = pygame.Rect(self.MARGIN + (column_wide * 3) + (self.COLUMN_H_PADDING * 3), self.MARGIN, column_wide,
                                   column_tall)

        self.CELL_HEIGHT = (column_tall - (self.STROKE * 2)) // 26

        self.FONT_SIZE = (self.CELL_HEIGHT * 22) // 28
        self.narrow_font = pygame.font.Font("fonts/AsapCondensed-Medium.ttf", self.FONT_SIZE)

        self.ICON_WIDTH = self.CELL_HEIGHT
        self.ICON_PADDING = 4
        icon_image = pygame.image.load('graphics/magazine_icon.png')
        self.magazine_icon = pygame.transform.smoothscale(icon_image, (self.ICON_WIDTH, self.ICON_WIDTH))
        self.magazine_icon = self.magazine_icon.convert_alpha()
        icon_image = pygame.image.load('graphics/magazine_icon_17.png')
        self.magazine_icon_17 = pygame.transform.smoothscale(icon_image, (self.ICON_WIDTH, self.ICON_WIDTH))
        self.magazine_icon_17 = self.magazine_icon_17.convert_alpha()
        icon_image = pygame.image.load('graphics/magazine_icon_33.png')
        self.magazine_icon_33 = pygame.transform.smoothscale(icon_image, (self.ICON_WIDTH, self.ICON_WIDTH))
        self.magazine_icon_33 = self.magazine_icon_33.convert_alpha()
        icon_image = pygame.image.load('graphics/magazine_icon_50.png')
        self.magazine_icon_50 = pygame.transform.smoothscale(icon_image, (self.ICON_WIDTH, self.ICON_WIDTH))
        self.magazine_icon_50 = self.magazine_icon_50.convert_alpha()
        icon_image = pygame.image.load('graphics/magazine_icon_67.png')
        self.magazine_icon_67 = pygame.transform.smoothscale(icon_image, (self.ICON_WIDTH, self.ICON_WIDTH))
        self.magazine_icon_67 = self.magazine_icon_67.convert_alpha()
        icon_image = pygame.image.load('graphics/magazine_icon_83.png')
        self.magazine_icon_83 = pygame.transform.smoothscale(icon_image, (self.ICON_WIDTH, self.ICON_WIDTH))
        self.magazine_icon_83 = self.magazine_icon_83.convert_alpha()
        icon_image = pygame.image.load('graphics/magazine_icon_100.png')
        self.magazine_icon_100 = pygame.transform.smoothscale(icon_image, (self.ICON_WIDTH, self.ICON_WIDTH))
        self.magazine_icon_100 = self.magazine_icon_100.convert_alpha()
        icon_image = pygame.image.load('graphics/bookmark_icon.png')
        self.bookmark_icon = pygame.transform.smoothscale(icon_image, (self.ICON_WIDTH, self.ICON_WIDTH))
        self.bookmark_icon = self.bookmark_icon.convert_alpha()
        chevron_image = pygame.image.load('graphics/chevron.png')
        self.chevron = pygame.transform.smoothscale(chevron_image, (self.ICON_WIDTH, self.ICON_WIDTH))
        self.chevron = self.chevron.convert_alpha()


    def _draw_row(self, item, text_x, text_y, selected, active, bounds, surface, is_file, progress, bookmark):
        if selected:
            # Make a copy of the original rect
            item_bounds = bounds.copy()
            item_bounds.height = self.CELL_HEIGHT
            item_bounds.y = text_y
            if active:
                pygame.draw.rect(surface, self.ACTIVE_COLOR, item_bounds)
            else:
                pygame.draw.rect(surface, self.INACTIVE_COLOR, item_bounds)

        if is_file:
            icon = self.magazine_icon
            if progress > 0:
                icon = self.magazine_icon_17
            if progress > 25:
                icon = self.magazine_icon_33
            if progress > 42:
                icon = self.magazine_icon_50
            if progress > 58:
                icon = self.magazine_icon_67
            if progress > 75:
                icon = self.magazine_icon_83
            if progress == 100:
                icon = self.magazine_icon_100
            surface.blit(icon, (text_x + self.TEXT_X_OFFSET, text_y + self.TEXT_Y_OFFSET))
            if bookmark:
                surface.blit(self.bookmark_icon, (text_x + self.TEXT_X_OFFSET, text_y + self.TEXT_Y_OFFSET))
            text_x += self.ICON_WIDTH + self.ICON_PADDING
        elif selected:
            surface.blit(self.chevron, (bounds.right - self.ICON_WIDTH, text_y + self.TEXT_Y_OFFSET))

        if selected:
            text_surface = self.narrow_font.render(item, True, self.BLACK_TRANSPARENT)
        else:
            text_surface = self.narrow_font.render(item, True, self.WHITE)
        surface.blit(text_surface, (text_x + self.TEXT_X_OFFSET, text_y + self.TEXT_Y_OFFSET))


    def _draw_column(self, directories, files, selected_row, active, prefixes, column_index, surface):
        if column_index == 1:
            bounds = self.column_1
        elif column_index == 2:
            bounds = self.column_2
        elif column_index == 3:
            bounds = self.column_3
        else:
            bounds = self.column_4

        text_x = bounds.left
        text_y = bounds.top
        row = 0
        for item in directories:
            item_name = item
            if column_index > 1:
                for one_prefix in prefixes:
                    if (item_name.startswith(one_prefix)):
                        item_name = item_name[len(one_prefix):]
            self._draw_row(item_name, text_x, text_y, row == selected_row, active, bounds, surface, False, 0, False)
            if row == selected_row:
                prefixes.append(item)
            text_y = text_y + self.CELL_HEIGHT
            row = row + 1
        for item in files:
            progress = 0
            magazine_dict = self.progress_dictionary.get(item)
            if magazine_dict:
                progress = magazine_dict.get("percent_progress")
            has_bookmark = len(self.bookmark_dictionary.get(item) or {}) > 0
            item_name = item[:-4]  # Removes the last 4 characters ('.pdf')
            # Remove "prefix": any portion of text that matches an element in the path.
            for one_prefix in prefixes:
                if (item_name.startswith(one_prefix)):
                    item_name = item_name[len(one_prefix):]
            if (item_name.startswith(' - ')):
                item_name = item_name[3:]
            self._draw_row(item_name, text_x, text_y, row == selected_row, active, bounds, surface, True, progress, has_bookmark)
            text_y = text_y + self.CELL_HEIGHT
            row = row + 1


    def _prepare_surface(self, toc_data_source):
        prefixes = []
        active_column = toc_data_source.active_column

        # Draw the rounded rectangle
        pygame.draw.rect(self.surface, self.WHITE, (0, 0, self.width, self.toc_tall), border_radius=self.RADIUS)
        pygame.draw.rect(self.surface, self.BLACK_TRANSPARENT,
                         (self.STROKE, self.STROKE, self.width - (self.STROKE * 2), self.toc_tall - (self.STROKE * 2)),
                         border_radius=self.RADIUS - self.STROKE)

        # Draw column 1.
        directories, files, selected_row = toc_data_source.directories_and_files_for_column(1)
        self._draw_column(directories, files, selected_row, active_column == 1, prefixes, 1, self.surface)

        # Draw column 2.
        directories, files, selected_row = toc_data_source.directories_and_files_for_column(2)
        self._draw_column(directories, files, selected_row, active_column == 2, prefixes, 2, self.surface)

        # Draw column 3.
        directories, files, selected_row = toc_data_source.directories_and_files_for_column(3)
        self._draw_column(directories, files, selected_row, active_column == 3, prefixes, 3, self.surface)

        # Draw column 4.
        directories, files, selected_row = toc_data_source.directories_and_files_for_column(4)
        self._draw_column(directories, files, selected_row, active_column == 4, prefixes, 4, self.surface)


    @property
    def visible(self)->bool:
        return self._visible


    def handle(self)->bool:
        if (not self._visible) and (self.alpha > 0):
            elapsed_time = time.time() - self.start_time  # Handle fade-out timing
            if elapsed_time < self.FADE_TIME:
                self.alpha = int(255 * (self.FADE_TIME - elapsed_time))
            else:
                self.alpha = 0  # Fully faded out
            self.dirty = True
        return self.dirty


    def render(self, screen):
        self.surface.set_alpha(self.alpha)
        screen.blit(self.surface, (self.x_loc, self.y_loc))
        self.dirty = False


    def hide(self):
        self._visible = False
        self.start_time = time.time()  # Reset HUD visibility
        self.dirty = True


    def show(self, data_source):
        self._prepare_surface(data_source)
        self._visible = True
        self.alpha = 255
        self.dirty = True


    def toggle(self, data_source)->bool:
        self._visible = not self._visible
        if self._visible:
            self.show(data_source)
        else:
            self.hide()
        return self._visible


    def update(self, toc_data_source):
        self._prepare_surface(toc_data_source)
        self.dirty = True

