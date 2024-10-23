from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from src.database.database import Base


class Machinery(Base):
    __tablename__ = 'maquinaria_agricola'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column('nombre', String(100), nullable=False)
    description = Column('descripcion', Text, nullable=True)
    costPerHour = Column('costo_hora', Float, nullable=False)

    # Relación con OpMech
    operationMechanization = relationship("OpMech", back_populates="machinery")
