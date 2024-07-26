# import tensorflow as tf

# def load_train_data():
#     # Charger et préparer vos données annotées ici
#     pass

# train_data = load_train_data()

# model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
# model = tf.keras.Sequential([
#     model,
#     tf.keras.layers.GlobalAveragePooling2D(),
#     tf.keras.layers.Dense(1, activation='sigmoid')
# ])

# model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
#               loss=tf.keras.losses.BinaryCrossentropy(),
#               metrics=['accuracy'])

# model.fit(train_data, epochs=10)

# # model.save('license_plate_detector.h5')



import cv2
import pytesseract
from pytesseract import Output
import re
from datetime import datetime

# Définir le chemin de l'exécutable Tesseract si nécessaire
# pytesseract.pytesseract.tesseract_cmd = r'path_to_your_tesseract_executable'

# Charger l'image
image_path = '/mnt/data/script.png'  # Remplacez par le chemin de votre image
image = cv2.imread(image_path)

# Convertir l'image en niveaux de gris
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Appliquer un flou pour réduire le bruit
gray = cv2.medianBlur(gray, 5)

# Utiliser Tesseract pour effectuer la reconnaissance de texte
custom_config = r'--oem 3 --psm 6'
details = pytesseract.image_to_data(gray, output_type=Output.DICT, config=custom_config, lang='eng')

# Fonction pour détecter le pays en fonction du texte de la plaque
def detect_country(text):
    text = text.replace(" ", "")  # Supprimer les espaces
    if re.match(r"^[A-Z]{2}[0-9]{2}\s[A-Z]{3}$", text):
        return 'Royaume Uni'
    elif re.match(r"^[A-Z]{2}\s[0-9]{4}$", text):
        return 'Luxembourg'
    elif re.match(r"^[A-Z]{1}[A-Z0-9]{1}\s[A-Z]{1}\s[0-9]{4}$", text):
        return 'Allemagne'
    elif re.match(r"^[A-Z]{2}\-[0-9]{3}\-[A-Z]{2}$", text):
        return 'France'
    elif re.match(r"^[O]\-[A-Z]{3}\-[0-9]{3}$", text):
        return 'Belgique'
    elif re.match(r"^[A-Z]{1}\-[0-9]{3}\-[A-Z]{2}$", text):
        return 'Pays-Bas'
    else:
        return 'Inconnu'

# Boucle sur chaque mot détecté et détecter les pays
n_boxes = len(details['text'])
for i in range(n_boxes):
    if int(details['conf'][i]) > 60:  # Filtrer par confiance
        text = details['text'][i].strip()
        country = detect_country(text)
        (x, y, w, h) = (details['left'][i], details['top'][i], details['width'][i], details['height'][i])
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, country, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        print(f'Detected text: {text}, Country: {country}, Confidence: {details["conf"][i]}')

# Afficher l'image avec les rectangles dessinés
cv2.imshow('Detected License Plates', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
