import requests
from bs4 import BeautifulSoup
import os

# Configuration
URL = "https://dev.to/tags"
OUTPUT_FILE = "tag_list.txt"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def crawl_tags():
    print(f"Connecting to {URL}...")
    
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
    except Exception as e:
        print(f"Connection error: {e}")
        return

    print("Parsing HTML content...")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    found_tags = set() # Use a set to avoid duplicates

    # Logic: Find all <a> tags where href starts with '/t/' and text starts with '#'
    links = soup.find_all('a', href=True)
    
    for link in links:
        href = link['href']
        text = link.get_text().strip()
        
        if href.startswith('/t/') and text.startswith('#'):
            # Remove the '#' character and extra whitespace
            clean_tag = text.replace('#', '').strip()
            
            # Basic validation to ensure it is not empty
            if clean_tag:
                found_tags.add(clean_tag)

    # Sort tags alphabetically
    sorted_tags = sorted(list(found_tags))
    
    # Save to file
    if sorted_tags:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            for tag in sorted_tags:
                f.write(f"{tag}\n")
        
        print(f"Success! Saved {len(sorted_tags)} tags to '{OUTPUT_FILE}'.")
    else:
        print("No tags found. The website structure might have changed.")

if __name__ == "__main__":
    crawl_tags()