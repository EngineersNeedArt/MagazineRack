import fitz  # PyMuPDF


class Magazine:
    pdf_document = None
    total_pages = 0
    current_page = 1

    def __init__(self, path, initial_page=1):
        self.pdf_document = fitz.open(path)
        self.total_pages = self.pdf_document.page_count
        self.current_page = initial_page


    def get_document(self):
        return self.pdf_document


    def get_page_count(self):
        return self.total_pages


    def get_current_page(self)->int:
        return self.current_page


    def go_prev_page(self)->bool:
        if self.current_page > 1:
            self.current_page -= 2  # Move backward by 2 pages
            if self.current_page < 1:
                self.current_page = 1
            return True
        else:
            return False


    def go_next_page(self)->bool:
        if self.current_page < self.total_pages:
            if self.current_page == 1:
                self.current_page += 1
            else:
                self.current_page += 2  # Move forward by 2 pages
                if self.current_page > self.total_pages:
                    if self.total_pages % 2 == 0:
                        self.current_page = self.total_pages
                    else:
                        self.current_page = self.total_pages - 1
            return True
        else:
            return False

