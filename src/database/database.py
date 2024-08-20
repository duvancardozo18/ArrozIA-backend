from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


print("-------------------------")
print("-------------------------")
print("-------------------------")
print("-------------------------")
print("-------------------------")
DATABASE_URL = "postgresql://postgres:4tetodenos@localhost:5432/ArrozIADBPostgreSQL"

try:
    engine = create_engine(DATABASE_URL)
    # Intentar establecer una conexión para verificar la URL
    with engine.connect() as connection:
        print("Conexión a la base de datos establecida con éxito.")
except SQLAlchemyError as e:
    print(f"Error al conectar con la base de datos: {e}")

#engine = create_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal =  sessionmaker(bind=engine, expire_on_commit=False)

def get_session() ->str:
    session = SessionLocal()
    try:
        yield session
        
    finally:
        session.close()