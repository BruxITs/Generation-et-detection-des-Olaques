# Utilisez l'image officielle de Python comme image de base
FROM python:3.9

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers requirements.txt et install les dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application
COPY . .

# Exposer le port que FastAPI utilise
EXPOSE 8000

# Démarrer l'application FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
