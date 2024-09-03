from sqlalchemy import Column, Integer, String, Text
from src.database.database import Base 
class VariedadArroz(Base):
    __tablename__ = 'variedad_arroz'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    numero_registro_productor_ica = Column(Integer, nullable=False)
    siembra = Column(Text)
    caracteristicas_variedad = Column(Text)
    susceptibilidad_herbicidas = Column(Text)
    manejo_fitosanitario = Column(Text)
    fertilizacion_nutricion = Column(Text)
    cosecha = Column(Text)
    oferta_ambiental = Column(Text)
    recomendaciones_generales = Column(Text)

    