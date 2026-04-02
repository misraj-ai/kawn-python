import fitz
from concurrent.futures import ThreadPoolExecutor
from typing import Union, List, Optional
import os
from uuid import uuid1


def render_page(page_index: int, doc_path_or_bytes: Union[str, bytes], matrix: fitz.Matrix,
                output_folder: Optional[str] = None) -> Union[bytes, str]:
    """Helper function to render a single page in a separate thread."""
    # We open the doc inside the worker to ensure thread safety
    if isinstance(doc_path_or_bytes, bytes):
        doc = fitz.open("pdf", doc_path_or_bytes)
    else:
        doc = fitz.open(doc_path_or_bytes)

    page = doc.load_page(page_index)
    # colorspace="rgb" and alpha=False significantly speed up rendering
    pix = page.get_pixmap(matrix=matrix, colorspace=fitz.csRGB, alpha=False)

    if output_folder is not None:
        filename = os.path.join(output_folder, f"{uuid1()}_{page_index + 1}.png")
        pix.save(filename)
        result = filename
    else:
        result = pix.tobytes("png")

    doc.close()
    return result


def convert_pdf_to_images(pdf_content: Union[bytes, str], zoom: int = 4, output_folder: Optional[str] = None) -> List[
    Union[bytes, str]]:
    """
    Optimized conversion using parallel processing and optimized rendering settings.
    If output_folder is provided, the images are saved to disk and their file paths are returned.
    Otherwise, returns the raw image streams (bytes).
    """
    matrix = fitz.Matrix(zoom, zoom)

    if output_folder:
        os.makedirs(output_folder, exist_ok=True)

    # We open once just to get the page count
    if isinstance(pdf_content, str):
        with fitz.open(pdf_content) as doc:
            page_count = doc.page_count
    else:
        with fitz.open("pdf", pdf_content) as doc:
            page_count = doc.page_count

    # Parallelize the rendering of pages
    # Note: Use max_workers based on your CPU cores
    with ThreadPoolExecutor() as executor:
        # Pass pdf_content to each worker
        results = executor.map(
            lambda i: render_page(i, pdf_content, matrix, output_folder),
            range(page_count)
        )

    return list(results)