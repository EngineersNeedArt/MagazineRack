import fitz  # PyMuPDF
import io
from PIL import Image


class Magazine:
    def __init__(self, path, initial_page=1):
        self.pdf_document = fitz.open(path)
        self.total_pages = self.pdf_document.page_count
        self.current_page = initial_page
        self.rendered_pages = {}


    def _resize_image(self, img, max_width, max_height):
        img_width, img_height = img.size
        img_ratio = img_width / img_height
        max_ratio = max_width / max_height
        if img_ratio > max_ratio:
            new_width = max_width
            new_height = int(new_width / img_ratio)
        else:
            new_height = max_height
            new_width = int(new_height * img_ratio)
        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)


    def get_document(self):
        return self.pdf_document


    def get_page_count(self):
        return self.total_pages


    def get_current_page(self)->int:
        return self.current_page


    def image_for_page(self, page_num, max_width, max_height):
        if page_num in self.rendered_pages:
            return self.rendered_pages[page_num]
        else:
            page = self.pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            img_data = io.BytesIO(pix.tobytes("png"))
            img = Image.open(img_data)
            img = self._resize_image(img, max_width, max_height)
            self.rendered_pages[page_num] = img
            return img


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

