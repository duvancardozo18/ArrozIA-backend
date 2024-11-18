from sqlalchemy import Column, Date, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from src.database.database import Base
from src.models.cropModel import Crop

class Harvest(Base):
    __tablename__ = 'cosecha'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cultivo_id = Column(Integer, ForeignKey('cultivo.id'), nullable=False)
    fecha_estimada_cosecha = Column(Date, nullable=True)
    fecha_cosecha = Column(Date, nullable=True)
    precio_carga_mercado = Column(Float, nullable=False)
    gasto_transporte_cosecha = Column(Float, nullable=False)
    gasto_recoleccion = Column(Float, nullable=False)
    cantidad_producida_cosecha = Column(Float, nullable=False)
    venta_cosecha = Column(Float, nullable=False)

    crop = relationship("Crop", back_populates="harvests")