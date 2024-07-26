import random

def generate_license_plate(country: str) -> str:
    # Logique pour générer une plaque d'immatriculation selon le pays
    if country == "France":
        return f"{random.randint(100, 999)} {chr(random.randint(65, 90))}{chr(random.randint(65, 90))} {random.randint(10, 99)}"
    # Ajouter d'autres pays
    return "XXXXXXX"
