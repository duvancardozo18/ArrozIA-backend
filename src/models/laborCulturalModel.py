from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base
from src.models.phenologicalStageModel import PhenologicalStage  # Importa correctamente el modelo

class LaborCultural(Base):
    __tablename__ = 'labor_cultural'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)  # Máximo de 100 caracteres para el nombre
    descripcion = Column(Text, nullable=True)  # Campo opcional para la descripción
    precio_hectaria = Column(Numeric(10, 2), nullable=True)  # Precio por hectárea
    precio_hectaria_estimada = Column(Numeric(10, 2), nullable=True)  # Precio estimado por hectárea
    id_etapa_fenologica = Column(Integer, ForeignKey('etapa_fenologica.id'), nullable=True)  # Relación con etapa fenológica

    # Relación con PhenologicalStage
    etapa_fenologica = relationship(
        'PhenologicalStage',  # Modelo relacionado
        backref='labor_culturales',  # Relación inversa en PhenologicalStage
        lazy='joined'  # Carga inmediata de la relación
    )
    
    # Relación con Task
    tasks = relationship(
        'Task',  # Modelo Task
        back_populates='labor_cultural',  # Relación inversa definida en Task
        cascade='all, delete-orphan'  # Cascada para manejar la eliminación
    )
