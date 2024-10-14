import fitz  # PyMuPDF


pdf_document = None
total_pages = 0
current_page = 1


def init_magazine(path, initial_page=1):
    global pdf_document
    global total_pages
    global current_page
    pdf_document = fitz.open(path)
    total_pages = pdf_document.page_count
    current_page = initial_page
    return pdf_document


def get_magazine_document():
    global pdf_document
    return pdf_document


def get_magazine_page_count():
    global total_pages
    return total_pages


def get_current_magazine_page()->int:
    global current_page
    return current_page


def left_magazine_event()->bool:
    global current_page
    if current_page > 1:
        current_page -= 2  # Move backward by 2 pages
        if current_page < 1:
            current_page = 1
        return True
    else:
        return False


def right_magazine_event()->bool:
    global total_pages
    global current_page
    if current_page < total_pages:
        if current_page == 1:
            current_page += 1
        else:
            current_page += 2  # Move forward by 2 pages
            if current_page > total_pages:
                if total_pages % 2 == 0:
                    current_page = total_pages
                else:
                    current_page = total_pages - 1
        return True
    else:
        return False

