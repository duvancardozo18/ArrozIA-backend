from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database.database import Base
from src.models.landModel import Land
from src.models.varietyArrozModel import VarietyArrozModel
from src.models.weightUnitModel import WeightUnit


class Crop(Base):
    __tablename__ = 'cultivo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cropName = Column('nombre_cultivo', String(100), nullable=False)
    varietyId = Column('variedad_id', Integer, ForeignKey('variedad_arroz.id'), nullable=False)
    plotId = Column('lote_id', Integer, ForeignKey('lote.id'), nullable=False)
    plantingDate = Column('fecha_siembra', Date, nullable=True)
    estimatedHarvestDate = Column('fecha_estimada_cosecha', Date, nullable=True)
    slug = Column(String, unique=True, index=True)

    # Relaciones
    variety = relationship("VarietyArrozModel", back_populates="crops")
    lotes = relationship("Land", back_populates="crops")
    tasks = relationship("Task", back_populates="cultivo")  # Nueva relación
    monitorings = relationship("Monitoring", back_populates="crop")  # Relación hacia monitoreos
    diagnosticos = relationship("DiagnosticoFitosanitario", back_populates="cultivo") # Relación inversa con DiagnosticoFitosanitario
    agricultural_inputs = relationship("AgriculturalInput", back_populates="cultivo")  # Relación inversa
    harvests = relationship("Harvest", back_populates="crop")  # Relación inversa con Cosecha
    gastos = relationship("Costs", back_populates="cultivo")