import os
from PIL import Image
from tqdm import tqdm

countries = ['Belgique', 'France', 'Allemagne', 'Luxembourg', 'Pays-Bas', 'Royaume-Uni']
data_dir = 'images'

def annotate_images():
    for country in countries:
        images_dir = os.path.join(data_dir, country)
        annotated_dir = os.path.join(data_dir, f'{country}_annotated')
        os.makedirs(annotated_dir, exist_ok=True)
        
        for filename in tqdm(os.listdir(images_dir)):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                image_path = os.path.join(images_dir, filename)
                img = Image.open(image_path)
                
                annotated_filename = f'{country}_{filename}'
                annotated_path = os.path.join(annotated_dir, annotated_filename)
                img.save(annotated_path)

if __name__ == '__main__':
    annotate_images()
