from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.database.database import Base

# Modelo AgriculturalInput
class AgriculturalInput(Base):
    __tablename__ = 'insumo_agricola'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    unidad_id = Column(Integer, ForeignKey("unidad_insumo.id"), nullable=False)
    costo_unitario = Column(Float, nullable=False)
    cantidad = Column(Float, nullable=False)

    # Relación con la tabla de unidad_insumo
    unidad = relationship("UnidadInsumo", back_populates="insumos")

# Modelo UnidadInsumo
class UnidadInsumo(Base):
    __tablename__ = 'unidad_insumo'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)

    # Relación inversa para acceder a los insumos
    insumos = relationship("AgriculturalInput", back_populates="unidad")
