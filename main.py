import os
import pdfplumber
import logging
from concurrent.futures import ThreadPoolExecutor
import requests
from get_metadata import extract_metadata

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL to request summary and keywords
summarizer_url = "http://127.0.0.1:8000/summarize/"

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

def processor(pdf_path):
    """
    Extract metadata from a single PDF file and process it.
    """
    try:
        logging.info(f"Processing {pdf_path}...")

        # Extract metadata
        metadata = extract_metadata(pdf_path)
        
        # Extract text from PDF
        pdf_text = extract_text_from_pdf(pdf_path)
        
        # Check if text extraction was successful
        if not pdf_text.strip():
            logging.warning(f"No text extracted from {pdf_path}")
            return
        
        # Correct payload structure
        summary_payload = {
            "text": str(pdf_text),
            "metadata": metadata
        }


        # Make the request
        response = requests.post(summarizer_url, json=summary_payload)
        
        # Check if the response is successful
        if response.status_code == 200:
            logging.info(f"Successfully processed {pdf_path} and stored in MongoDB")
        else:
            logging.error(f"Failed to process {pdf_path}. Status code: {response.status_code}")
            logging.error(response.text)

    except Exception as e:
        logging.error(f"Error processing {pdf_path}: {str(e)}")

def process_pdfs_concurrently(folder_path):
    """
    Process all PDFs in the folder concurrently.
    """
    pdf_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(".pdf")]

    logging.info(f"Found {len(pdf_files)} PDF files in {folder_path}")
    
    with ThreadPoolExecutor() as executor:
        executor.map(processor, pdf_files)

# specify the folder and run the driver function
folder_path = "test_pdfs"
process_pdfs_concurrently(folder_path)
