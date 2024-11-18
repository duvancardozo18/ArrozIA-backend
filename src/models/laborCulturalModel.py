from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base
from src.models.phenologicalStageModel import PhenologicalStage  # Importa correctamente el modelo

class LaborCultural(Base):
    __tablename__ = 'labor_cultural'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)  # Máximo de 100 caracteres
    descripcion = Column(Text, nullable=True)
    precio_hectaria = Column(Numeric(10, 2), nullable=True)  # Ajustado a precio_hectaria
    precio_hectaria_estimada = Column(Numeric(10, 2), nullable=True)  # Ajustado a precio_hectaria_estimada
    id_etapa_fenologica = Column(Integer, ForeignKey('etapa_fenologica.id'), nullable=True)

    # Relación con la tabla PhenologicalStage
    etapa_fenologica = relationship(
        'PhenologicalStage',  # Modelo relacionado
        backref='labor_culturales',  # Relación inversa en PhenologicalStage
        lazy='joined'  # Carga inmediata de la relación
    )
