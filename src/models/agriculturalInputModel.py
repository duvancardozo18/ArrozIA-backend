from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database.database import Base


# Modelo UNI_INPUT
class UNI_INPUT(Base):
    __tablename__ = 'unidad_insumo'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)

    # Relación con insumo_agricola
    insumos_agricolas = relationship("AgriculturalInput", back_populates="unidad")

# Modelo AgriculturalInput
class AgriculturalInput(Base):
    __tablename__ = 'insumo_agricola'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    unidad_id = Column(Integer, ForeignKey('unidad_insumo.id'), nullable=False)
    costo_unitario = Column(Float, nullable=False)

    # Relación con unidad_insumo
    unidad = relationship("UNI_INPUT", back_populates="insumos_agricolas")
