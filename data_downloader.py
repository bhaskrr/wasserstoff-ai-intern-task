import json
import os
import requests

# Load the JSON file
with open('Dataset.json', 'r') as file:
    data = json.load(file)

# Define a folder to save the downloaded files
save_folder = 'data'

# Loop through the JSON and download each file
for i, (key, url) in enumerate(data.items(), start=1):
    try:
        # Send a request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        
        # Create a filename based on the key or index
        filename = os.path.join(save_folder, f'file_{i}_{key}.pdf')
        
        # Save the file
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"Downloaded: {filename}")
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")
