import pdfplumber
import os

def extract_metadata(pdf_path):
    """
    Extract file name, file path, file size in kb and number of pages from a pdf
    """
    file_name = os.path.basename(pdf_path)
    file_size = os.path.getsize(pdf_path) / 1024
    metadata = {
        "file_name": file_name,
        "file_path": pdf_path,
        "file_size_kb": file_size,
    }
    try:
        with pdfplumber.open(pdf_path) as pdf:
            metadata["num_pages"] = len(pdf.pages)
    except Exception as e:
        metadata["error"] = str(e)
    return metadata

# folder_path = 'data'

# get_metadata(folder_path)