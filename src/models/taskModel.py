from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Numeric
from src.database.database import Base

class Task(Base):
    __tablename__ = "tarea_labor_cultural"

    id = Column(Integer, primary_key=True, index=True)
    fecha_estimada = Column(Date, nullable=False)
    fecha_realizacion = Column(Date, nullable=True)
    descripcion = Column(String, nullable=True)
    estado_id = Column(Integer, ForeignKey("estado.id", ondelete="CASCADE"), nullable=False)
    es_mecanizable = Column(Boolean, default=False)
    cultivo_id = Column(Integer, ForeignKey("cultivo.id", ondelete="CASCADE"), nullable=False)
    labor_cultural_id = Column(Integer, ForeignKey("labor_cultural.id", ondelete="CASCADE"), nullable=False)
    insumo_agricola_id = Column(Integer, ForeignKey("insumo_agricola.id", ondelete="SET NULL"), nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    cantidad_insumo = Column(Integer, nullable=True)
    maquinaria_agricola_id = Column(Integer, ForeignKey("maquinaria_agricola.id", ondelete="SET NULL"), nullable=True)
    precio_labor_cultural = Column(Numeric(10, 2), nullable=True)  # Nueva columna añadida

    # Relación hacia Crop (cultivo)
    cultivo = relationship("Crop", back_populates="tasks")

    # Relación hacia AgriculturalInput (insumo agrícola)
    insumo_agricola = relationship("AgriculturalInput", back_populates="tasks")

    # Relación hacia labor cultural (labor-cultural)
    labor_cultural = relationship("LaborCultural", back_populates="tasks")

    # Relación hacia User (usuario)
    usuario = relationship("User", back_populates="tasks")

    # Relación con Machinery
    maquinaria_agricola = relationship("Machinery", back_populates="tasks")

    # Relación con Estado (nombre del estado)
    estado = relationship("Estado", back_populates="tasks")
