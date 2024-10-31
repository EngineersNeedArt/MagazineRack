import fitz  # PyMuPDF
import io
from PIL import Image
import threading


# Turn on or off background threading of the rendering/caching of PDF pages.
THREADED_RENDERING = False


class Magazine:
    def __init__(self, path, initial_page=1):
        self._pdf_document = fitz.open(path)
        self._page_count = self._pdf_document.page_count
        if (not initial_page) or (initial_page > self._page_count):
            initial_page = 1
        self._current_page = initial_page
        self._rendered_pages = {}
        if THREADED_RENDERING:
            self._rendering_pages = {}
            self._cache_lock = threading.Lock()


    def _calculate_image_size(self, image):
        width, height = image.size
        channels = len(image.getbands())  # e.g., 3 for RGB, 4 for RGBA
        return width * height * channels  # bytes per pixel is assumed to be 1 byte per channel


    def _cache_memory_usage(self, cache):
        total_size = 0
        for page_num, image in cache.items():
            total_size += self._calculate_image_size(image)
        return total_size


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


    def _render_pdf_page(self, page_num, max_width, max_height):
        page = self._pdf_document.load_page(page_num)
        zoom = 2.0  # Increase this value to get better quality (2.0 = 200% zoom, 3.0 = 300%, etc.)
        matrix = fitz.Matrix(zoom, zoom)  # Create a transformation matrix for scaling
        pix = page.get_pixmap(matrix=matrix)
        img_data = io.BytesIO(pix.tobytes("png"))
        img = Image.open(img_data)
        img = self._resize_image(img, max_width, max_height)
        if THREADED_RENDERING:
            with self._cache_lock:
                self._rendered_pages[page_num] = img
                del self._rendering_pages[page_num]
        else:
            self._rendered_pages[page_num] = img
        # total_cache_size = self._cache_memory_usage(self._rendered_pages)
        # print(f"Total memory used by cache: {total_cache_size / (1024 ** 2):.2f} MB")


    def _fetch_image_for_page(self, page_num, max_width, max_height):
        thread = threading.Thread(target=self._render_pdf_page, args=(page_num, max_width, max_height))
        thread.daemon = True
        thread.start()


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
        img = None
        if THREADED_RENDERING:
            with self._cache_lock:
                if page_num in self._rendered_pages:
                    img = self._rendered_pages[page_num]
                else:
                    if not page_num in self._rendering_pages:
                        self._rendering_pages[page_num] = True
                        self._fetch_image_for_page(page_num, max_width, max_height)
        else:
            if page_num in self._rendered_pages:
                img = self._rendered_pages[page_num]
            else:
                self._render_pdf_page(page_num, max_width, max_height)
                img = self._rendered_pages[page_num]
        return img


    def go_prev_page(self)->bool:
        was_page = self._current_page
        if self._current_page > 1:
            self._current_page -= 2  # Move backward by 2 pages
            if self._current_page < 1:
                self._current_page = 1
        return self._current_page != was_page


    def go_next_page(self)->bool:
        was_page = self._current_page
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
        return self._current_page != was_page

