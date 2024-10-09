import os

directory_path = None
base_directories = []
base_files = []

def init_TOC_Data(base_path):
    global directory_path
    global base_directories
    global base_files

    directory_path = base_path

    # Get a list of file and directory names
    contents = os.listdir(directory_path)

    for item in contents:
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            base_directories.append(item)
        elif item_path.endswith('.pdf'):
            base_files.append(item)

def left_TOC_event()->bool:
    return True

def right_TOC_event()->bool:
    return True

def up_TOC_event()->bool:
    return True

def down_TOC_event()->bool:
    return True