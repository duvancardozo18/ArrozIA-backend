from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from typing import Generator
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

try:
    engine = create_engine(DATABASE_URL)
    # Intentar establecer una conexión para verificar la URL
    with engine.connect() as connection:
        print("Conexión a la base de datos establecida con éxito.")
except SQLAlchemyError as e:
    print(f"Error al conectar con la base de datos: {e}")

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
