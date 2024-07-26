import requests
from bs4 import BeautifulSoup
import os
import urllib.request

# URLs des galeries Platesmania
urls = {
    "Belgique": "https://platesmania.com/be/gallery",
    "France": "https://platesmania.com/fr/gallery",
    "Allemagne": "https://platesmania.com/de/gallery",
    "Luxembourg": "https://platesmania.com/lu/gallery",
    "Royaume-Uni": "https://platesmania.com/uk/gallery",
    "Pays-Bas": "https://platesmania.com/nl/gallery"
}

# Répertoire pour stocker les images
data_dir = "data/plates"

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_image(url, path):
    try:
        urllib.request.urlretrieve(url, path)
        print(f"Downloaded {url} to {path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def scrape_gallery(url, country):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    for img in img_tags:
        img_url = img['src']
        if img_url.startswith('http'):
            img_name = img_url.split('/')[-1]
            img_path = os.path.join(data_dir, country, img_name)
            download_image(img_url, img_path)

# Créer les répertoires pour chaque pays
for country in urls.keys():
    create_directory(os.path.join(data_dir, country))

# Scraper chaque galerie
for country, url in urls.items():
    print(f"Scraping gallery for {country}")
    scrape_gallery(url, country)
