from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()

class DetectionResult(Base):
    __tablename__ = "detection_results"
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(255), index=True)
    country = Column(String(255), index=True)
    accuracy = Column(Float)
    timestamp = Column(DateTime)

class GenerationResult(Base):
    __tablename__ = "generation_results"
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(255), index=True)
    generated_plate = Column(String(255))
    timestamp = Column(DateTime)

# URL de connexion à la base de données
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/license_plate_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

# Initialiser la base de données
init_db()
