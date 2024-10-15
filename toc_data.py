import os


class TOC_Data:

    def __init__(self, base_path):
        self.directory_path = base_path
        self.directories_column_1 = []
        self.files_column_1 = []
        self.directories_column_2 = []
        self.files_column_2 = []
        self.directories_column_3 = []
        self.files_column_3 = []
        self.directories_column_4 = []
        self.files_column_4 = []
        self._get_directories_and_files_for_column(1)
        self.active_column = 0
        self.column_1_selected_row = None
        self.column_2_selected_row = None
        self.column_3_selected_row = None
        self.column_4_selected_row = None
        self.selection_changed = False


    @staticmethod
    def _path_is_directory(path) -> bool:
        return os.path.isdir(path)


    def _get_directory_path_for_column(self, column_index):
        path = self.directory_path
        if column_index == 1:
            return path

        if (self.column_1_selected_row is not None) and (
                self.column_1_selected_row < (len(self.directories_column_1) + len(self.files_column_1))):
            if self.column_1_selected_row < len(self.directories_column_1):
                last_component = self.directories_column_1[self.column_1_selected_row]
            else:
                last_component = self.files_column_1[self.column_1_selected_row - len(self.directories_column_1)]
            path = os.path.join(path, last_component)
        if column_index == 2:
            return path

        if (self.column_2_selected_row is not None) and (
                self.column_2_selected_row < (len(self.directories_column_2) + len(self.files_column_2))):
            if self.column_2_selected_row < len(self.directories_column_2):
                last_component = self.directories_column_2[self.column_2_selected_row]
            else:
                last_component = self.files_column_2[self.column_2_selected_row - len(self.directories_column_2)]
            path = os.path.join(path, last_component)
        if column_index == 3:
            return path

        if (self.column_3_selected_row is not None) and (
                self.column_3_selected_row < (len(self.directories_column_3) + len(self.files_column_3))):
            if self.column_3_selected_row < len(self.directories_column_3):
                last_component = self.directories_column_3[self.column_3_selected_row]
            else:
                last_component = self.files_column_3[self.column_3_selected_row - len(self.directories_column_3)]
            path = os.path.join(path, last_component)
        if column_index == 4:
            return path

        if (self.column_4_selected_row is not None) and (
                self.column_4_selected_row < (len(self.directories_column_4) + len(self.files_column_4))):
            if self.column_4_selected_row < len(self.directories_column_4):
                last_component = self.directories_column_4[self.column_4_selected_row]
            else:
                last_component = self.files_column_4[self.column_4_selected_row - len(self.directories_column_4)]
            path = os.path.join(path, last_component)
        return path


    def _get_directories_files_at_path(self, path):
        directories = []
        files = []

        if (path is not None) and TOC_Data._path_is_directory(path):
            contents = os.listdir(path)
            for item in contents:
                item_path = os.path.join(path, item)
                if TOC_Data._path_is_directory(item_path):
                    directories.append(item)
                elif item_path.endswith('.pdf'):
                    files.append(item)
            directories.sort()
            files.sort()
        return directories, files


    def _get_directories_and_files_for_column(self, column_index):
        path = self._get_directory_path_for_column(column_index)
        if column_index == 1:
            self.directories_column_1, self.files_column_1 = self._get_directories_files_at_path(path)
        elif column_index == 2:
            self.directories_column_2, self.files_column_2 = self._get_directories_files_at_path(path)
        elif column_index == 3:
            self.directories_column_3, self.files_column_3 = self._get_directories_files_at_path(path)
        elif column_index == 4:
            self.directories_column_4, self.files_column_4 = self._get_directories_files_at_path(path)


    def _select_start(self):
        self.active_column = 1
        self.column_1_selected_row = 0
        self.selection_changed = True
        self.column_2_selected_row = None
        self._get_directories_and_files_for_column(2)
        return True


    def _select_end(self):
        self.active_column = 1
        self.column_1_selected_row = self._count_directories_files_for_column(1) - 1
        self.selection_changed = True
        self.column_2_selected_row = None
        self._get_directories_and_files_for_column(2)
        return True


    def _clear_column(self, column_index):
        global directories_column_2
        global files_column_2
        global directories_column_3
        global files_column_3
        global directories_column_4
        global files_column_4

        if column_index == 2:
            self.directories_column_2.clear()
            self.files_column_2.clear()
        if column_index == 3:
            self.directories_column_3.clear()
            self.files_column_3.clear()
        if column_index == 4:
            self.directories_column_4.clear()
            self.files_column_4.clear()


    def _left_active_column(self):
        if self.active_column == 0:
            return self._select_start()

        # Retard to active column to left.
        if self.active_column > 1:
            self.active_column = self.active_column - 1

        if self.active_column == 1:
            self.column_2_selected_row = None
            self._clear_column(3)
            self.selection_changed = True
            return True

        if self.active_column == 2:
            self.column_3_selected_row = None
            self._clear_column(4)
            self.selection_changed = True
            return True

        if self.active_column == 3:
            self.column_4_selected_row = None
            self.selection_changed = True
            return True
        return False


    def _right_active_column(self):
        # No column is active yet.
        if self.active_column == 0:
            return self._select_start()

        # Advance to column to right.
        if self.active_column < 4:
            next_column = self.active_column + 1
        row_count = self._count_directories_files_for_column(next_column)
        if row_count == 0:
            return False

        self.active_column = next_column

        if self.active_column == 2:
            self.column_2_selected_row = 0
            self.selection_changed = True
            self._get_directories_and_files_for_column(3)
            return True

        if self.active_column == 3:
            self.column_3_selected_row = 0
            self.selection_changed = True
            self._get_directories_and_files_for_column(4)
            return True

        if self.active_column == 4:
            self.column_4_selected_row = 0
            self.selection_changed = True
            return True
        return False


    def _up_active_column(self):
        if self.active_column == 0:
            return self._select_end()

        if self.active_column == 1:
            if self.column_1_selected_row > 0:
                self.column_1_selected_row -= 1
                self.selection_changed = True
            else:
                return False

            self.column_2_selected_row = None
            self._get_directories_and_files_for_column(2)
            return True

        if self.active_column == 2:
            if self.column_2_selected_row > 0:
                self.column_2_selected_row -= 1
                self.selection_changed = True
            else:
                return False

            self.column_3_selected_row = None
            self._get_directories_and_files_for_column(3)
            return True

        if self.active_column == 3:
            if self.column_3_selected_row > 0:
                self.column_3_selected_row -= 1
                self.selection_changed = True
            else:
                return False

            self.column_4_selected_row = None
            self._get_directories_and_files_for_column(4)
            return True

        if self.active_column == 4:
            if self.column_4_selected_row > 0:
                self.column_4_selected_row -= 1
                self.selection_changed = True
            else:
                return False
            return True
        return False


    def _down_active_column(self):
        if self.active_column == 0:
            return self._select_start()

        if self.active_column == 1:
            num_rows = self._count_directories_files_for_column(1)
            if (self.column_1_selected_row + 1) < num_rows:
                self.column_1_selected_row += 1
                self.selection_changed = True
            else:
                return False

            self.column_2_selected_row = None
            self._get_directories_and_files_for_column(2)
            return True

        if self.active_column == 2:
            num_rows = self._count_directories_files_for_column(2)
            if (self.column_2_selected_row + 1) < num_rows:
                self.column_2_selected_row += 1
                self.selection_changed = True
            else:
                return False

            self.column_3_selected_row = None
            self._get_directories_and_files_for_column(3)
            return True

        if self.active_column == 3:
            num_rows = self._count_directories_files_for_column(3)
            if (self.column_3_selected_row + 1) < num_rows:
                self.column_3_selected_row += 1
                self.selection_changed = True
            else:
                return False

            self.column_4_selected_row = None
            self._get_directories_and_files_for_column(4)
            return True

        if self.active_column == 4:
            num_rows = self._count_directories_files_for_column(4)
            if (self.column_4_selected_row + 1) < num_rows:
                self.column_4_selected_row += 1
                self.selection_changed = True
            else:
                return False
            return True
        return False


    def _count_directories_files_for_column(self, column_index):
        if column_index == 1:
            return len(self.directories_column_1) + len(self.files_column_1)
        if column_index == 2:
            return len(self.directories_column_2) + len(self.files_column_2)
        if column_index == 3:
            return len(self.directories_column_3) + len(self.files_column_3)
        if column_index == 4:
            return len(self.directories_column_4) + len(self.files_column_4)
        return 0


    def directories_and_files_for_column(self, column_index):
        if column_index == 1:
            return self.directories_column_1, self.files_column_1, self.column_1_selected_row
        elif column_index == 2:
            return self.directories_column_2, self.files_column_2, self.column_2_selected_row
        elif column_index == 3:
            return self.directories_column_3, self.files_column_3, self.column_3_selected_row
        elif column_index == 4:
            return self.directories_column_4, self.files_column_4, self.column_4_selected_row


    def did_selection_change(self)->bool:
        return self.selection_changed


    def selected_path(self):
        return self._get_directory_path_for_column(0)


    def get_active_column(self)->int:
        return self.active_column


    def go_left(self)->bool:
        return self._left_active_column()


    def go_right(self)->bool:
        return self._right_active_column()


    def go_up(self)->bool:
        return self._up_active_column()


    def go_down(self)->bool:
        return self._down_active_column()

