# from sqlalchemy import Column, Integer, String, Text, ForeignKey
# from sqlalchemy.orm import relationship
# from src.database.database import Base

# class Monitoring(Base):
#     __tablename__ = "monitoreos"
    
#     id = Column(Integer, primary_key=True, index=True)
#     tipo = Column(String(100), nullable=False)
#     variedad_arroz_etapa_fenologica_id = Column(Integer, ForeignKey("variedad_arroz_etapa_fenologica.id"), nullable=True)
#     recomendacion = Column(Text)
#     crop_id = Column(Integer, ForeignKey("cultivo.id"), nullable=False)  # Nueva columna de relación con Crop

#     # Relación hacia la tabla variedad_arroz_etapa_fenologica
#     variedad_arroz_etapa_fenologica = relationship("VarietyRiceStageModel", back_populates="monitoreos")

#     # Relación hacia la tabla cultivo
#     crop = relationship("Crop", back_populates="monitorings")  # Definir la relación hacia Crop

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, SmallInteger
from sqlalchemy.orm import relationship
from src.database.database import Base

class Monitoring(Base):
    __tablename__ = "monitoreos"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(100), nullable=False)
    variedad_arroz_etapa_fenologica_id = Column(Integer, ForeignKey("variedad_arroz_etapa_fenologica.id"), nullable=True)
    recomendacion = Column(Text)
    crop_id = Column(Integer, ForeignKey("cultivo.id"), nullable=False)  # Relación con Crop
    
    # Nuevos campos
    fecha_programada = Column(Date, nullable=False)  # Fecha estimada asignada por el administrador
    fecha_finalizacion = Column(Date, nullable=True)  # Fecha real de finalización
    estado = Column(SmallInteger, nullable=False, default=1)  # 1: Pendiente, 2: Terminado
    
    # Relación hacia la tabla variedad_arroz_etapa_fenologica
    variedad_arroz_etapa_fenologica = relationship("VarietyRiceStageModel", back_populates="monitoreos")

    # Relación hacia la tabla cultivo
    crop = relationship("Crop", back_populates="monitorings")  # Relación con Crop
