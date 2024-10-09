import fitz  # PyMuPDF
import io
from PIL import Image

# Cache for rasterized PDF pages
rendered_pages = {}
pdf_document = None


def set_pdf_document(document):
    global pdf_document
    pdf_document = document
    rendered_pages.clear()


def _resize_image(img, max_width, max_height):
    img_width, img_height = img.size
    img_ratio = img_width / img_height
    max_ratio = max_width / max_height

    if img_ratio > max_ratio:
        new_width = max_width
        new_height = int(new_width / img_ratio)
    else:
        new_height = max_height
        new_width = int(new_height * img_ratio)

    return img.resize((new_width, new_height), Image.LANCZOS)

# Render page to image and cache it
def render_page_to_image(page_num, max_width, max_height):
    global pdf_document

    if page_num in rendered_pages:
        return rendered_pages[page_num]

    page = pdf_document.load_page(page_num)
    pix = page.get_pixmap()
    img_data = io.BytesIO(pix.tobytes("png"))
    img = Image.open(img_data)
    img = _resize_image(img, max_width, max_height)
    rendered_pages[page_num] = img
    return img

