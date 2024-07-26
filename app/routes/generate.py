from PIL import Image, ImageDraw, ImageFont
import random
import string
import os
from datetime import datetime
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models import SessionLocal, GenerationResult

router = APIRouter()

# Dépendance pour obtenir la session de la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PlateRequest(BaseModel):
    country: str

@router.post("/generate")
async def generate_plate(request: PlateRequest, db: Session = Depends(get_db)):
    try:
        def generate_unique_plate(existing_plates):
            """Génère une plaque unique qui n'existe pas dans la base de données."""
            while True:
                plate = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
                if plate not in existing_plates:
                    return plate

        # Récupérer les plaques existantes pour vérifier l'unicité
        existing_plates = db.query(GenerationResult.generated_plate).all()
        existing_plates = {plate[0] for plate in existing_plates}

        # Générer une plaque unique
        generated_plate = generate_unique_plate(existing_plates)

        # Dimensions de l'image
        width, height = 680, 120  # Largeur augmentée à 680 pixels
        background_color = (255, 204, 0)  # Couleur de fond (jaune)
        font_color = (0, 0, 0)  # Couleur du texte (noir)
        square_color = (0, 0, 255)  # Couleur du carré (bleu)

        # Charger une police pour le texte
        font_path = "font/DejaVuSans-Bold.ttf"  # Chemin vers une police disponible dans votre projet
        font = ImageFont.truetype(font_path, 90)
        small_font = ImageFont.truetype(font_path, 50)  # Police plus petite pour les initiales

        # Créer l'image
        image = Image.new("RGB", (width, height), background_color)
        draw = ImageDraw.Draw(image)

        # Ajouter le carré bleu avec les initiales du pays
        square_width = 200  # Largeur du carré bleu augmentée pour assurer la visibilité du texte
        square_x = 0
        square_y = 0
        draw.rectangle([square_x, square_y, square_x + square_width, height], fill=square_color)

        # Ajouter les initiales du pays dans le carré
        initials = request.country[:2].upper()  # Utiliser les 2 premières lettres du pays
        text_bbox = draw.textbbox((0, 0), initials, font=small_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = square_x + (square_width - text_width) / 2
        text_y = (height - text_height) / 2
        draw.text((text_x, text_y), initials, font=small_font, fill=(255, 255, 255))  # Couleur du texte (blanc)

        # Ajouter le texte de la plaque d'immatriculation
        text_bbox = draw.textbbox((0, 0), generated_plate, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = square_width + 20  # Espace entre le carré et le texte
        text_y = (height - text_height) / 2
        draw.text((text_x, text_y), generated_plate, font=font, fill=font_color)

        # Définir le chemin pour sauvegarder l'image
        output_dir = "data/plates/generate"
        os.makedirs(output_dir, exist_ok=True)
        image_path = os.path.join(output_dir, f"{generated_plate}.png")
        image.save(image_path)

        # Sauvegarde dans la base de données
        generation_result = GenerationResult(
            country=request.country,
            generated_plate=generated_plate,
            timestamp=datetime.utcnow()
        )
        db.add(generation_result)
        db.commit()
        db.refresh(generation_result)

        return {
            "country": request.country,
            "generated_plate": generated_plate,
            "image_path": image_path,
            "id": generation_result.id
        }
    except IntegrityError:
        db.rollback()  # En cas de conflit d'intégrité, annuler les changements
        raise HTTPException(status_code=500, detail="Un problème est survenu lors de la génération de la plaque.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
