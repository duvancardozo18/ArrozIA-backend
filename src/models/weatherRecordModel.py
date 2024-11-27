from sqlalchemy import Column, Integer, Date, Float, ForeignKey, String, Text, Time
from src.database.database import Base
from sqlalchemy.orm import relationship

class WeatherRecord(Base):
    __tablename__ = "registro_meteorologico"

    id = Column(Integer, primary_key=True, index=True)
    lote_id = Column(Integer, ForeignKey('lote.id'), nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=True)  # Cambiado a nullable=True para permitir None
    temperatura = Column(Float, nullable=False)
    presion_atmosferica = Column(Float, nullable=False)
    humedad = Column(Float, nullable=False)
    precipitacion = Column(Float)
    indice_ultravioleta = Column(Float, nullable=False)
    horas_sol = Column(Float, nullable=False)
    fuente_datos = Column(String, nullable=False)  # Indica si el origen fue "manual" o "api"
    api_respuesta = Column(Text, nullable=True)    # Guarda la respuesta completa de la API (solo para registros de la API

    lote = relationship("Land", back_populates="weather_records")  # Aquí está la relación inversa