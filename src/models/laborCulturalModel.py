from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base
from src.models.phenologicalStageModel import PhenologicalStage  # Importa el modelo con el nombre correcto

class LaborCultural(Base):
    __tablename__ = 'labor_cultural'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio_hora_real = Column(Numeric(10, 2), nullable=True)
    precio_hora_estimado = Column(Numeric(10, 2), nullable=True)
    id_etapa_fenologica = Column(Integer, ForeignKey('etapa_fenologica.id'), nullable=True)

    # Relación con la tabla PhenologicalStage
    etapa_fenologica = relationship('PhenologicalStage', backref='labor_culturales', lazy='joined')
