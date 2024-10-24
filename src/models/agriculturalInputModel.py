from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database.database import Base

# Modelo AgriculturalInput
class AgriculturalInput(Base):
    __tablename__ = 'insumo_agricola'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    unidad = Column(String(255), nullable=True)
    costo_unitario = Column(Float, nullable=False)


   
