import os

directory_path = None
directories_column_1 = []
files_column_1 = []
directories_column_2 = []
files_column_2 = []
directories_column_3 = []
files_column_3 = []
directories_column_4 = []
files_column_4 = []
active_column = 0
column_1_selected_row = None
column_2_selected_row = None
column_3_selected_row = None
column_4_selected_row = None
selection_changed = False


def _get_directory_path_for_column (column_index):
    global directory_path
    global directories_column_1
    global directories_column_2
    global directories_column_3
    global column_1_selected_row
    global column_2_selected_row
    global column_3_selected_row

    path = directory_path
    if column_index == 1:
        return path

    if (column_1_selected_row is not None) and (column_1_selected_row < len(directories_column_1)):
        path = os.path.join(path, directories_column_1[column_1_selected_row])
    else:
        path = None

    if column_index == 2:
        return path

    if (column_2_selected_row is not None) and (column_2_selected_row < len(directories_column_2)):
        path = os.path.join(path, directories_column_2[column_2_selected_row])
    else:
        path = None

    if column_index == 3:
        return path

    if (column_3_selected_row is not None) and (column_3_selected_row < len(directories_column_3)):
        path = os.path.join(path, directories_column_3[column_3_selected_row])
    else:
        path = None
    return path


def _get_directories_files_at_path(path):
    directories = []
    files = []

    if path is not None:
        contents = os.listdir(path)
        for item in contents:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                directories.append(item)
            elif item_path.endswith('.pdf'):
                files.append(item)
        directories.sort()
        files.sort()
    return directories, files


def _get_column_1_directories_and_files():
    global directories_column_1
    global files_column_1
    path = _get_directory_path_for_column(1)
    directories_column_1, files_column_1 = _get_directories_files_at_path(path)


def _get_column_2_directories_and_files():
    global directories_column_2
    global files_column_2
    path = _get_directory_path_for_column(2)
    directories_column_2, files_column_2 = _get_directories_files_at_path(path)


def _get_column_3_directories_and_files():
    global directories_column_3
    global files_column_3
    path = _get_directory_path_for_column(3)
    directories_column_3, files_column_3 = _get_directories_files_at_path(path)


def _get_column_4_directories_and_files():
    global directories_column_4
    global files_column_4
    path = _get_directory_path_for_column(4)
    directories_column_4, files_column_4 = _get_directories_files_at_path(path)


def _select_start():
    global active_column
    global column_1_selected_row
    global column_2_selected_row
    global selection_changed
    active_column = 1
    column_1_selected_row = 0
    selection_changed = True
    column_2_selected_row = None
    _get_column_2_directories_and_files()
    return True


def _select_end():
    global active_column
    global column_1_selected_row
    global column_2_selected_row
    global selection_changed
    active_column = 1
    column_1_selected_row = _count_directories_files_for_column(1) - 1
    selection_changed = True
    column_2_selected_row = None
    _get_column_2_directories_and_files()
    return True


def _left_active_column():
    global active_column
    global column_2_selected_row
    global column_3_selected_row
    global column_4_selected_row
    global selection_changed

    if active_column == 0:
        return _select_start()

    # Retard to active column to left.
    if active_column > 1:
        active_column = active_column - 1

    if active_column == 1:
        column_2_selected_row = None
        selection_changed = True
        return True

    if active_column == 2:
        column_3_selected_row = None
        selection_changed = True
        return True

    if active_column == 3:
        column_4_selected_row = None
        selection_changed = True
        return True

    return False

def _right_active_column():
    global active_column
    global column_1_selected_row
    global column_2_selected_row
    global column_3_selected_row
    global column_4_selected_row
    global selection_changed

    # No column is active yet.
    if active_column == 0:
        return _select_start()

    # Advance to column to right.
    if active_column < 4:
        next_column = active_column + 1

    row_count = _count_directories_files_for_column(next_column)
    if row_count == 0:
        return False

    active_column = next_column

    if active_column == 2:
        column_2_selected_row = 0
        selection_changed = True
        _get_column_3_directories_and_files()
        return True

    if active_column == 3:
        column_3_selected_row = 0
        selection_changed = True
        _get_column_4_directories_and_files()
        return True

    if active_column == 4:
        column_4_selected_row = 0
        selection_changed = True
        return True

    return False


def _up_active_column():
    global active_column
    global column_1_selected_row
    global column_2_selected_row
    global column_3_selected_row
    global column_4_selected_row
    global selection_changed

    if active_column == 0:
        return _select_end()

    if active_column == 1:
        if column_1_selected_row > 0:
            column_1_selected_row = column_1_selected_row - 1
            selection_changed = True
        else:
            return False

        column_2_selected_row = None
        _get_column_2_directories_and_files()
        return True

    if active_column == 2:
        if column_2_selected_row > 0:
            column_2_selected_row = column_2_selected_row - 1
            selection_changed = True
        else:
            return False

        column_3_selected_row = None
        _get_column_3_directories_and_files()
        return True

    if active_column == 3:
        if column_3_selected_row > 0:
            column_3_selected_row = column_3_selected_row - 1
            selection_changed = True
        else:
            return False

        column_4_selected_row = None
        _get_column_4_directories_and_files()
        return True

    if active_column == 4:
        if column_4_selected_row > 0:
            column_3_selected_row = column_4_selected_row - 1
            selection_changed = True
        else:
            return False
        return True

    return False


def _down_active_column():
    global active_column
    global column_1_selected_row
    global column_2_selected_row
    global column_3_selected_row
    global column_4_selected_row
    global selection_changed

    if active_column == 0:
        return _select_start()

    if active_column == 1:
        num_rows = _count_directories_files_for_column(1)
        if (column_1_selected_row + 1) < num_rows:
            column_1_selected_row = column_1_selected_row + 1
            selection_changed = True
        else:
            return False

        column_2_selected_row = None
        _get_column_2_directories_and_files()
        return True

    if active_column == 2:
        num_rows = _count_directories_files_for_column(2)
        if (column_2_selected_row + 1) < num_rows:
            column_2_selected_row = column_2_selected_row + 1
            selection_changed = True
        else:
            return False

        column_3_selected_row = None
        _get_column_3_directories_and_files()
        return True

    if active_column == 3:
        num_rows = _count_directories_files_for_column(3)
        if (column_3_selected_row + 1) < num_rows:
            column_3_selected_row = column_3_selected_row + 1
            selection_changed = True
        else:
            return False

        column_4_selected_row = None
        _get_column_4_directories_and_files()
        return True

    if active_column == 4:
        num_rows = _count_directories_files_for_column(4)
        if (column_4_selected_row + 1) < num_rows:
            column_4_selected_row = column_4_selected_row + 1
            selection_changed = True
        else:
            return False
        return True

    return False


def _count_directories_files_for_column (column_index):
    global directories_column_1
    global files_column_1
    global directories_column_2
    global files_column_3
    global directories_column_3
    global files_column_3
    global directories_column_4
    global files_column_4

    if column_index == 1:
        return len(directories_column_1) + len(files_column_1)
    if column_index == 2:
        return len(directories_column_2) + len(files_column_2)
    if column_index == 3:
        return len(directories_column_3) + len(files_column_3)
    if column_index == 4:
        return len(directories_column_4) + len(files_column_4)
    return 0


def init_TOC_Data(base_path):
    global directory_path
    global directories_column_1
    global files_column_1

    directory_path = base_path
    _get_column_1_directories_and_files()


def get_TOC_column_1_directories_files():
    global directories_column_1
    global files_column_1
    return directories_column_1, files_column_1, column_1_selected_row


def get_TOC_column_2_directories_files():
    global directories_column_2
    global files_column_2
    return directories_column_2, files_column_2, column_2_selected_row


def get_TOC_column_3_directories_files():
    global directories_column_3
    global files_column_3
    return directories_column_3, files_column_3, column_3_selected_row


def is_TOC_selection_changed()->bool:
    global selection_changed
    return selection_changed


def selected_TOC_path():
    global directories_column_1
    global column_1_selected_row
    return directories_column_1[column_1_selected_row]


def left_TOC_event()->bool:
    return _left_active_column()


def right_TOC_event()->bool:
    return _right_active_column()


def up_TOC_event()->bool:
    return _up_active_column()


def down_TOC_event()->bool:
    return _down_active_column()

