![PDF Image](image.jpg)

# PDF Processing Pipeline Documentation

## Project Overview

This project implements a PDF processing pipeline using Python to extract metadata, summaries, and keywords from PDF documents. The pipeline leverages several libraries, including pdfplumber, transformers, and MongoDB, and is designed to efficiently handle multiple PDFs concurrently.

## Key Features:

- Extracts metadata, including file name, file path, size, number of pages.
- Utilizes a summarization pipeline from transformers library to generate summaries of PDF content.
- Implements keyword extraction using KeyBERT.
- Stores processed data in a MongoDB database.

## Installation

This project requires Python and several external libraries. Follow the instructions below to set up the environment.
### Prerequisites:

- Python 3.x

### Required Libraries:

You need to install the following libraries:

   Ensure you have Python and pip installed on your system. You can check by running:

   ```shell copy
      python --version
      pip --version
   ```
   - For the API:
     1. Navigate to the directory `api` using terminal/command prompt:

      ```shell copy
         cd api
      ```

     2. Install the required packages using pip:

      ```shell copy
         pip install -r requirements.txt
      ```
   
      **Note**: To use a mongodb database, create a `.env` file in the `api` directory and store the database connection url as a constant named `DB_URL`.


- For Metadata Extraction:
   - In the root folder of the project, run:
   ```shell
      pip install -r requirements.txt
   ```
This will read the requirements.txt file and install all the listed dependencies.

## Usage

To run the PDF processing pipeline, follow these steps:

1. Store PDF files in a folder on your local machine. (In this case, the test_pdfs folder contains three pdfs with different lengths).
2. Specify the folder path in the script where your PDFs are stored(e.g. test_pdfs).
3. Run the script to process the PDFs. The pipeline will extract the necessary metadata and store it in MongoDB while logging the details in a file.
4. To run the script, navigate to the root folder of the project and run:
   
   ```shell
      python3 main.py
   ```
**Note**: Make sure the API is running before sending a request.
   
To run the API, follow these steps:

   1. Navigate to the `api` folder, and run:
   
      ```shell copy
         uvicorn main:app --reload
      ```

Here’s how to use the pipeline:

### Functionalities

1. **Metadata Extraction**:

   Extracts the following metadata from each PDF:
   - File Name
   - File Path
   - File Size (KB)
   - Number of Pages
   - Processing Time in seconds (after summarizing and extracting keywords)

2. **Summarization**:

   Utilizes a pre-trained model from the transformers library to generate a concise summary from the content
   of the PDF text.

3. **Keyword Extraction**:

   Uses KeyBERT from sentence_transformers library to extract the top five keywords present in the PDF document.

4. **Data Storage**:

   Stores the extracted metadata, summary, and keywords in a MongoDB database for easy retrieval and analysis.

5. **Logging**:

   Processing details are logged into the console.

## Code Structure

The primary components of the code include:

- Logging Configuration: Sets up the logging for tracking the processing of PDF files.
- MongoDB Setup: Configures the connection to MongoDB for storing extracted data.
- PDF Processing Functions.

## Troubleshooting
Common Issues:

- MongoDB Connection Errors: Verify your MongoDB connection string and ensure your database is accessible.
- PDF Extraction Issues: Ensure that the PDFs are not corrupted and can be read by pdfplumber.

Debugging Tips:

- Add print statements to track the flow of execution and verify which parts of the code are running.
- Check for exceptions in the output to understand where errors might occur.

## Conclusion

This PDF processing pipeline provides an efficient way to extract valuable information from PDF documents, leveraging modern NLP techniques for summarization and keyword extraction.