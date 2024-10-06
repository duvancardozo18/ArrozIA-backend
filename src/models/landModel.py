from sqlalchemy import DECIMAL, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database.database import Base


class Land(Base):
    __tablename__ = 'lote'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    finca_id = Column(Integer, ForeignKey('finca.id'), nullable=False)
    area = Column(Float, nullable=False)
    # unidad_area_id = Column(Integer, ForeignKey('unidad_area.id'), nullable=False)
    latitud = Column(DECIMAL(10, 5), nullable=True)
    longitud = Column(DECIMAL(10, 5), nullable=True)
    
    # Relaciones
    finca = relationship("Farm", back_populates="lotes")   
    #unidad_area = relationship("UnidadArea", back_populates="lotes")
    crops = relationship("Crop", back_populates="lotes") 


# class UnidadArea(Base):
#     __tablename__ = 'unidad_area'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     unidad = Column(String(50), nullable=False)

    # Relación inversa
    #lotes = relationship("Land", order_by=Land.id, back_populates="unidad_area")

