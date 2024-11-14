from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.database import Base

class Agua(Base):
    __tablename__ = 'agua'

    id = Column(Integer, primary_key=True, index=True)
    costo_instalacion_agua_real = Column(Integer, nullable=True)
    costo_instalacion_agua_estimado = Column(Integer, nullable=True)
    costo_consumo_agua_real = Column(Integer, nullable=True)
    costo_consumo_agua_estimado = Column(Integer, nullable=True)
    consumo_energia_real = Column(Integer, nullable=True)
    consumo_energia_estimada = Column(Integer, nullable=True)

    # Relación bidireccional con VariableCost
    gastos_variables = relationship("VariableCost", back_populates="agua")

    def __repr__(self):
        return f"<Agua(id={self.id}, costo_instalacion_agua_real={self.costo_instalacion_agua_real})>"
