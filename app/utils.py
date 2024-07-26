from PIL import Image
import numpy as np

def read_imagefile(file) -> Image.Image:
    img = Image.open(file)
    return img

def prepare_image(img: Image.Image):
    img = img.resize((224, 224))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array
