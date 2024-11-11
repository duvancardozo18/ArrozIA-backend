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
    cultivo_id = Column(Integer, ForeignKey("cultivo.id"), nullable=False)  # Nueva clave foránea
    costo_unitario = Column(Float, nullable=False)
    precio_unitario_estimado = Column(Float, nullable=True)  # Nuevo campo para el costo estimado
    cantidad = Column(Float, nullable=False)
    cantidad_estimada = Column(Float, nullable=True)  # Nuevo campo para la cantidad estimada

    # Relación con la tabla de unidad_insumo
    unidad = relationship("UnidadInsumo", back_populates="insumos")
    cultivo = relationship("Crop", back_populates="agricultural_inputs")  # Relación con Crop

# Modelo UnidadInsumo
class UnidadInsumo(Base):
    __tablename__ = 'unidad_insumo'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)

    # Relación inversa para acceder a los insumos
    insumos = relationship("AgriculturalInput", back_populates="unidad")
