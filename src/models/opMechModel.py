from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from src.database.database import Base
from src.models.taskModel import Task
from src.models.machineryModel import Machinery


class OpMech(Base):
    __tablename__ = 'operacion_mecanizacion'

    id = Column(Integer, primary_key=True, autoincrement=True)
    taskId = Column('tarea_labor_id', Integer, ForeignKey('tarea_labor_cultural.id'), nullable=False)
    mechanizationName = Column('nombre_mecanizacion', String(50), nullable=False)
    machineryId = Column('maquinaria_id', Integer, ForeignKey('maquinaria_agricola.id'), nullable=False)
    hoursUsed = Column('horas_uso', Numeric(5, 2), nullable=False)

    # Relaciones
    task = relationship("Task", back_populates="operationMechanization")
    machinery = relationship("Machinery", back_populates="operationMechanization")
