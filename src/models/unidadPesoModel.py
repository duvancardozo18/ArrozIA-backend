from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.database import Base

class UnidadPeso(Base):
    __tablename__ = 'unidad_peso'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_unidad = Column(String(50), nullable=False)

    # Relación inversa con Cultivo
    cultivos = relationship("Cultivo", back_populates="unidad_peso")
