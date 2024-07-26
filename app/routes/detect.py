from fastapi import APIRouter, UploadFile, File, HTTPException
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import requests
from bs4 import BeautifulSoup
import shutil
import os
from PIL import Image
from urllib.request import urlretrieve

router = APIRouter()

# Mettez à jour ce chemin en fonction de votre installation de Tesseract
pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_CMD', r'C:\Program Files\Tesseract-OCR\tesseract.exe')

urls = {
    "Pays-Bas": "https://platesmania.com/nl/gallery",
    "Belgique": "https://platesmania.com/be/gallery",
    "France": "https://platesmania.com/fr/gallery",
    "Allemagne": "https://platesmania.com/de/gallery",
    "Luxembourg": "https://platesmania.com/lu/gallery",
    "Royaume-Uni": "https://platesmania.com/uk/gallery"
}

data_dir = "data/plates"

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def clear_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def download_image(url, path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        with open(path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {url} to {path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def scrape_first_page(url, country):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img', class_='img-responsive center-block margin-bottom-10')
        for img in img_tags:
            img_url = img['src']
            if img_url.startswith('http'):
                img_name = img_url.split('/')[-1]
                img_path = os.path.join(data_dir, country, img_name)
                download_image(img_url, img_path)
    else:
        print(f"Failed to retrieve {url}")

def scrape_paged_gallery(base_url, country):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    max_pages=10
    page_num = 1
    while page_num <= max_pages:
        page_url = f"{base_url}-{page_num}" if page_num > 1 else base_url
        print(f"Scraping {page_url} for {country}")
        response = requests.get(page_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve {page_url}")
            break
        
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img', class_='img-responsive center-block margin-bottom-10')
        
        if not img_tags:  # Stop if no images found
            print(f"No more images on {page_url}")
            break
        
        for img in img_tags:
            img_url = img['src']
            if img_url.startswith('http'):
                img_name = img_url.split('/')[-1]
                img_path = os.path.join(data_dir, country, img_name)
                download_image(img_url, img_path)
        
        page_num += 1

def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    custom_config = r'--oem 3 --psm 6'
    details = pytesseract.image_to_data(gray, output_type=Output.DICT, config=custom_config, lang='eng')
    text_plaque = ''
    for data in details['text']:
        if len(data) > 3:
            text_plaque = data
            print(text_plaque, "text")
    return text_plaque

@router.post("/detect")
async def detect_plate(file: UploadFile = File(...)):
    try:
        temp_file = f"/tmp/{file.filename}"
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        detected_text = extract_text_from_image(temp_file)
        
        for country, base_url in urls.items():
            print(f"Processing images from {country}")
            country_dir = os.path.join(data_dir, country)
            create_directory(country_dir)
            
            # Scrape the first page without pagination
            scrape_first_page(base_url, country)
            
            # Scrape subsequent pages with pagination
            scrape_paged_gallery(base_url, country)
            
            for img_file in os.listdir(country_dir):
                img_path = os.path.join(country_dir, img_file)
                scraped_text = extract_text_from_image(img_path)
                if detected_text == scraped_text:
                    os.remove(temp_file)  # Nettoyage du fichier temporaire
                    return {
                        "detected_plate": detected_text,
                        "country": country
                    }

        os.remove(temp_file)  # Nettoyage du fichier temporaire
        return {
            "detected_plate": detected_text,
            "country": "Unknown"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Vous pouvez également supprimer les fichiers temporaires dans le bloc finally si nécessaire
        print("Process completed")
