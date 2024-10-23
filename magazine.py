import fitz  # PyMuPDF
import io
from PIL import Image


class Magazine:
    def __init__(self, path, initial_page=1):
        self._pdf_document = fitz.open(path)
        self._page_count = self._pdf_document.page_count
        if (not initial_page) or (initial_page > self._page_count):
            initial_page = 1
        self._current_page = initial_page
        self._rendered_pages = {}


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


    @property
    def page_count(self) -> int:
        return self._page_count


    @property
    def current_page(self) -> int:
        return self._current_page


    def is_last_page(self) -> bool:
        if (self._page_count % 2) == 0:
            return self._current_page >= self._page_count
        else:
            return self._current_page >= self._page_count - 1


    def image_for_page(self, page_num, max_width, max_height):
        if page_num in self._rendered_pages:
            return self._rendered_pages[page_num]
        else:
            page = self._pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            img_data = io.BytesIO(pix.tobytes("png"))
            img = Image.open(img_data)
            img = self._resize_image(img, max_width, max_height)
            self._rendered_pages[page_num] = img
            return img


    def go_prev_page(self)->bool:
        if self._current_page > 1:
            self._current_page -= 2  # Move backward by 2 pages
            if self._current_page < 1:
                self._current_page = 1
            return True
        else:
            return False


    def go_next_page(self)->bool:
        if self._current_page < self._page_count:
            if self._current_page == 1:
                self._current_page += 1
            else:
                self._current_page += 2  # Move forward by 2 pages
                if self._current_page > self._page_count:
                    if self._page_count % 2 == 0:
                        self._current_page = self._page_count
                    else:
                        self._current_page = self._page_count - 1
            return True
        else:
            return False

