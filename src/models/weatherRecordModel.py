from sqlalchemy import Column, Integer, Date, Float, ForeignKey
from src.database.database import Base

class WeatherRecord(Base):
    __tablename__ = "registro_meteorologico"

    id = Column(Integer, primary_key=True, index=True)
    lote_id = Column(Integer, ForeignKey('lote.id'), nullable=False)
    fecha = Column(Date, nullable=False)
    temperatura = Column(Float, nullable=False)
    presion_atmosferica = Column(Float, nullable=False)
    humedad = Column(Float, nullable=False)
    precipitacion = Column(Float)
    indice_ultravioleta = Column(Float, nullable=False)
    horas_sol = Column(Float, nullable=False)
