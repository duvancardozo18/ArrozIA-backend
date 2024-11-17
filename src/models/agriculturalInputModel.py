from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.database.database import Base

class AgriculturalInput(Base):
    __tablename__ = 'insumo_agricola'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    unidad_id = Column(Integer, ForeignKey("unidad_insumo.id"), nullable=False)
    cultivo_id = Column(Integer, ForeignKey("cultivo.id"), nullable=False)
    costo_unitario = Column(Float, nullable=False)
    precio_unitario_estimado = Column(Float, nullable=True)
    cantidad = Column(Float, nullable=False)
    cantidad_estimada = Column(Float, nullable=True)
    tipo_insumo_id = Column(Integer, ForeignKey("tipo_insumo.id"), nullable=True)

    # Relaciones
    unidad = relationship("UnidadInsumo", back_populates="insumos")
    cultivo = relationship("Crop", back_populates="agricultural_inputs")
    tipo_insumo = relationship("TipoInsumo", back_populates="insumos")
    tasks = relationship("Task", back_populates="insumo_agricola")  # Relación inversa hacia Task


class UnidadInsumo(Base):
    __tablename__ = 'unidad_insumo'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)

    # Relación inversa para acceder a los insumos
    insumos = relationship("AgriculturalInput", back_populates="unidad")


class TipoInsumo(Base):
    __tablename__ = 'tipo_insumo'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)

    # Relación inversa para acceder a los insumos
    insumos = relationship("AgriculturalInput", back_populates="tipo_insumo")
