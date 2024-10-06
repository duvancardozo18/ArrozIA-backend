from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from src.database.database import Base

class VariedadArroz(Base):
    __tablename__ = 'variedad_arroz'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    numero_registro_productor_ica = Column(Integer, nullable=False)
    caracteristicas_variedad = Column(Text)
 

    # Relación inversa
    crops = relationship("Crop", order_by="Crop.id", back_populates="variety")