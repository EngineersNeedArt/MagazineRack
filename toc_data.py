import os
from pathlib import Path

class TOCData:

    def __init__(self, base_path, initial_path):
        self._directory_path = base_path
        self.directories_column_1 = []
        self.files_column_1 = []
        self.directories_column_2 = []
        self.files_column_2 = []
        self.directories_column_3 = []
        self.files_column_3 = []
        self.directories_column_4 = []
        self.files_column_4 = []
        self._get_directories_and_files_for_column(1)
        self._active_column = 0
        self.column_1_selected_row = None
        self.column_2_selected_row = None
        self.column_3_selected_row = None
        self.column_4_selected_row = None
        self.selection_changed = False
        if initial_path:
            self._selectInitialPath(base_path, initial_path)


    def _selectInitialPath(self, base_path, initial_path):
        path = Path(initial_path)
        components = list(path.parts)
        if components[0] == base_path:
            if len(components) <= 1:
                return
            row = self._row_matching(1, components[1])
            if row is not None:
                self._active_column = 1
                self.column_1_selected_row = row
                self._get_directories_and_files_for_column(2)
                if len(components) <= 2:
                    return
                row = self._row_matching(2, components[2])
                if row is not None:
                    self._active_column = 2
                    self.column_2_selected_row = row
                    self._get_directories_and_files_for_column(3)
                    if len(components) <= 3:
                        return
                    row = self._row_matching(3, components[3])
                    if row is not None:
                        self._active_column = 3
                        self.column_3_selected_row = row
                        self._get_directories_and_files_for_column(4)
                    if len(components) <= 4:
                        return
                    row = self._row_matching(4, components[4])
                    if row is not None:
                        self._active_column = 4
                        self.column_4_selected_row = row


    def _row_matching(self, column_index, component):
        if column_index == 1:
            directories = self.directories_column_1
            files = self.files_column_1
        elif column_index == 2:
            directories = self.directories_column_2
            files = self.files_column_2
        elif column_index == 3:
            directories = self.directories_column_3
            files = self.files_column_3
        elif column_index == 4:
            directories = self.directories_column_4
            files = self.files_column_4
        else:
            return None

        index = 0
        for item in directories:
            if item == component:
                return index
            index += 1
        for item in files:
            if item == component:
                return index
            index += 1
        return None


    def _get_directory_path_for_column(self, column_index):
        path = self._directory_path
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

        if (path is not None) and os.path.isdir(path):
            contents = os.listdir(path)
            for item in contents:
                if not item.startswith('.'):
                    item_path = os.path.join(path, item)
                    if os.path.isdir(item_path):
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
        self._active_column = 1
        self.column_1_selected_row = 0
        self.selection_changed = True
        self.column_2_selected_row = None
        self._get_directories_and_files_for_column(2)
        return True


    def _select_end(self):
        self._active_column = 1
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
        if self._active_column == 0:
            return self._select_start()

        # Retard to active column to left.
        if self._active_column > 1:
            self._active_column -= 1

        if self._active_column == 1:
            self.column_2_selected_row = None
            self._clear_column(3)
            self.selection_changed = True
            return True

        if self._active_column == 2:
            self.column_3_selected_row = None
            self._clear_column(4)
            self.selection_changed = True
            return True

        if self._active_column == 3:
            self.column_4_selected_row = None
            self.selection_changed = True
            return True
        return False


    def _right_active_column(self):
        # No column is active yet.
        if self._active_column == 0:
            return self._select_start()

        # Already all the way to the right.
        if self._active_column >= 4:
            return False

        # Advance to column to right.
        next_column = self._active_column + 1
        row_count = self._count_directories_files_for_column(next_column)
        if row_count == 0:
            return False

        self._active_column = next_column

        if self._active_column == 2:
            self.column_2_selected_row = 0
            self.selection_changed = True
            self._get_directories_and_files_for_column(3)
            return True

        if self._active_column == 3:
            self.column_3_selected_row = 0
            self.selection_changed = True
            self._get_directories_and_files_for_column(4)
            return True

        if self._active_column == 4:
            self.column_4_selected_row = 0
            self.selection_changed = True
            return True
        return False


    def _up_active_column(self):
        if self._active_column == 0:
            return self._select_end()

        if self._active_column == 1:
            if self.column_1_selected_row > 0:
                self.column_1_selected_row -= 1
                self.selection_changed = True
            else:
                return False

            self.column_2_selected_row = None
            self._get_directories_and_files_for_column(2)
            return True

        if self._active_column == 2:
            if self.column_2_selected_row > 0:
                self.column_2_selected_row -= 1
                self.selection_changed = True
            else:
                return False

            self.column_3_selected_row = None
            self._get_directories_and_files_for_column(3)
            return True

        if self._active_column == 3:
            if self.column_3_selected_row > 0:
                self.column_3_selected_row -= 1
                self.selection_changed = True
            else:
                return False

            self.column_4_selected_row = None
            self._get_directories_and_files_for_column(4)
            return True

        if self._active_column == 4:
            if self.column_4_selected_row > 0:
                self.column_4_selected_row -= 1
                self.selection_changed = True
            else:
                return False
            return True
        return False


    def _down_active_column(self):
        if self._active_column == 0:
            return self._select_start()

        if self._active_column == 1:
            num_rows = self._count_directories_files_for_column(1)
            if (self.column_1_selected_row + 1) < num_rows:
                self.column_1_selected_row += 1
                self.selection_changed = True
            else:
                return False

            self.column_2_selected_row = None
            self._get_directories_and_files_for_column(2)
            return True

        if self._active_column == 2:
            num_rows = self._count_directories_files_for_column(2)
            if (self.column_2_selected_row + 1) < num_rows:
                self.column_2_selected_row += 1
                self.selection_changed = True
            else:
                return False

            self.column_3_selected_row = None
            self._get_directories_and_files_for_column(3)
            return True

        if self._active_column == 3:
            num_rows = self._count_directories_files_for_column(3)
            if (self.column_3_selected_row + 1) < num_rows:
                self.column_3_selected_row += 1
                self.selection_changed = True
            else:
                return False

            self.column_4_selected_row = None
            self._get_directories_and_files_for_column(4)
            return True

        if self._active_column == 4:
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


    @property
    def selected_path(self):
        return self._get_directory_path_for_column(0)


    @property
    def active_column(self)->int:
        return self._active_column


    def go_left(self)->bool:
        return self._left_active_column()


    def go_right(self)->bool:
        return self._right_active_column()


    def go_up(self)->bool:
        return self._up_active_column()


    def go_down(self)->bool:
        return self._down_active_column()


    @staticmethod
    def is_directory(path)->bool:
        return os.path.isdir(path)

