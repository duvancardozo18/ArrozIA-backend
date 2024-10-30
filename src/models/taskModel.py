from sqlalchemy import Column, Date, ForeignKey, Integer, Boolean, Text
from sqlalchemy.orm import relationship
from src.database.database import Base


class Task(Base):
    __tablename__ = 'tarea_labor_cultural'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fechaEstimada = Column('fecha_estimada', Date, nullable=False)
    fechaRealizacion = Column('fecha_realizacion', Date, nullable=False)
    descripcion = Column('descripcion', Text, nullable=False)
    estadoId = Column('estado_id', Integer, ForeignKey('estado.id'), nullable=False)
    planeadaAutomaticamente = Column('planeada_automaticamente', Boolean, nullable=False)
    esMecanizable = Column('es_mecanizable', Boolean, nullable=False)
    cultivoId = Column('cultivo_id', Integer, ForeignKey('cultivo.id'), nullable=False)
    laborId = Column('labor_id', Integer, ForeignKey('labor_cultural.id'), nullable=False)
    insumoId = Column('insumo_id', Integer, ForeignKey('insumo_agricola.id'), nullable=False)
    manoObraId = Column('mano_obra_id', Integer, ForeignKey('mano_obra.id'), nullable=False)

    # Relación con OpMech
    operationMechanization = relationship("OpMech", back_populates="task")
