from sqlalchemy import DECIMAL, Column, Float, Integer, String
from sqlalchemy.orm import relationship

from src.database.database import Base
from src.models.landModel import Land


class Farm(Base):
    __tablename__ = 'finca'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    ubicacion = Column(String(100), nullable=True)
    area_total = Column(Float, nullable=True)
    latitud = Column(DECIMAL(10, 5), nullable=True)
    longitud = Column(DECIMAL(10, 5), nullable=True)
    
    lotes = relationship(Land, back_populates="finca")
    #usuario_fincas = relationship("UsuarioFinca", back_populates="finca")
