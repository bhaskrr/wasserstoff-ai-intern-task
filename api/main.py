from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from keybert import KeyBERT
import re
import asyncio
from pymongo import MongoClient
import logging
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()
summarizer = pipeline("summarization", model= "sshleifer/distilbart-cnn-12-6")
kw_model = KeyBERT()  # Initialize KeyBERT for keyword extraction


# MongoDB setup
db_url = os.getenv("DB_URL")
client = MongoClient(db_url)
db = client["pdf_database"]
collection = db["pdf_metadata"]

# Function to clean the input text
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = text.strip()  # Trim leading and trailing whitespace
    text = re.sub(r'[^\x20-\x7E]', '', text)  # Remove non-printable characters
    return text

# Function to split text into chunks based on max token limit
def split_text_into_chunks(text, max_length=1024):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(' '.join(current_chunk + [word])) <= max_length:
            current_chunk.append(word)
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

# Function to extract keywords from the text
def extract_keywords(text, num_keywords=5):
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=num_keywords)
    return [kw[0] for kw in keywords]

# Async function to summarize a chunk of text
async def summarize_chunk(chunk):
    summary = summarizer(chunk, max_length=30, min_length=20, do_sample=False)
    return summary[0]['summary_text']

# pydantic model to validate incoming data
class Input(BaseModel):
    text: str
    metadata: dict

# API endpoint to summarize text and extract keywords
@app.post("/summarize/")
async def summarize_extract_keywords_and_save(input: Input):
    
    metadata = input.metadata
    
    init_time = time.time()
    
    cleaned_text = clean_text(input.text)
    
    if not cleaned_text:
        raise HTTPException(status_code=400, detail="No valid text provided.")

    # Split text into manageable chunks
    text_chunks = split_text_into_chunks(cleaned_text, max_length=1024)

    try:
        # Create a list of asyncio tasks to summarize chunks concurrently
        tasks = [summarize_chunk(chunk) for chunk in text_chunks]
        
        # Run the tasks concurrently and wait for all to complete
        summaries = await asyncio.gather(*tasks)
        
        # Concatenate the summaries
        final_summary = " ".join(summaries)
        
        # Extract keywords from the cleaned text
        keywords = extract_keywords(cleaned_text)

        metadata["summary"] =  final_summary.strip()
        metadata["keywords"] = keywords
        comp_time = time.time() - init_time
        
        metadata["processing_time"] = comp_time
        
        # Save to MongoDB
        collection.insert_one(metadata)
        logging.info(f"A PDF has been processed and stored in MongoDB.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run the app:
# Save this code in a file (e.g., app.py) and run the following command:
# uvicorn app:app --reload
