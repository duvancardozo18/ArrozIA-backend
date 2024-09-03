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

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Verificar si DATABASE_URL se cargó correctamente
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está definida en el archivo .env")

try:
    engine = create_engine(DATABASE_URL)
    # Intentar establecer una conexión para verificar la URL
    with engine.connect() as connection:
        print("Conexión a la base de datos establecida con éxito.")
except SQLAlchemyError as e:
    print(f"Error al conectar con la base de datos: {e}")

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def get_db() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
