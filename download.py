import requests
import re
import os
import shutil

# Base URLs for the repository
GITHUB_REPO_URL = "https://raw.githubusercontent.com/v5tech/bing-wallpaper/main/"

# List of files to download directly from the main branch
DIRECT_FILES_TO_DOWNLOAD = ["README.md", "pom.xml"]

def download_file(url, file_name, force_download=False):
    """
    Downloads a file from a given URL and saves it.
    - If force_download is False and the file exists, it is skipped.
    - Returns True on successful download, False otherwise.
    """
    # Check if the file already exists and we are not forcing a download
    if not force_download and os.path.exists(file_name):
        print(f"🙂 File already exists, skipping download: {file_name}")
        return False

    print(f"Downloading: {file_name}")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Checks for HTTP errors
        
        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Download successful: {file_name}")
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"🥺 An issue occurred during download: {e}")
        
        if os.path.exists(file_name):
            print(f"❌ Download failed, but the file exists.")
        else:
            print(f"❌ Download failed and a backup of {file_name} was not found.")
        return False
            
def scrape_image_urls(file_path):
    """
    Reads a file and extracts all image URLs ending in .jpg, .png, .jpeg, or .gif.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"❌ File {file_path} not found.")
        return []

    image_urls = re.findall(r'(https?://[^\s]+\.(?:jpg|png|jpeg|gif))', content)
    return list(set(image_urls))

# --- Main Script ---
# Initializing counter for images
download_count = 0

# 1. Always download README.md and pom.xml
print("--- Downloading Core Files ---")
for file_name in DIRECT_FILES_TO_DOWNLOAD:
    url = GITHUB_REPO_URL + file_name
    download_file(url, file_name, force_download=True)

# 2. Scrape image URLs from the downloaded README.md
readme_file_path = "README.md"
image_urls = scrape_image_urls(readme_file_path)

if image_urls:
    print("\n--- Downloading Images ---")
    # 3. Download images only if they don't exist
    for i, url in enumerate(image_urls):
        match = re.search(r'id=([^&]+)', url)
        if match:
            full_filename = match.group(1)
            file_name = full_filename.replace('OHR.', '', 1)
        else:
            print(f"🥺 Could not extract a valid file name from URL: {url}")
            continue
        
        if download_file(url, file_name, force_download=False):
            download_count += 1
else:
    print("No images found in the README.md file.")

# Final Summary
print("\n--- Summary ---")
print(f"Downloaded {download_count} new image(s).")
print("\nProgram finished.")
