from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.database import Base

class VariedadArroz(Base):
    __tablename__ = 'variedad_arroz'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    numero_registro_productor_ica = Column(String, nullable=False)
    siembra = Column(String, nullable=True)
    caracteristicas_variedad = Column(String, nullable=True)
    susceptibilidad_herbicidas = Column(String, nullable=True)
    manejo_fitosanitario = Column(String, nullable=True)
    fertilizacion_nutricion = Column(String, nullable=True)
    cosecha = Column(String, nullable=True)
    oferta_ambiental = Column(String, nullable=True)
    recomendaciones_generales = Column(String, nullable=True)

    # Relación inversa
    cultivos = relationship("Cultivo", back_populates="variedad")