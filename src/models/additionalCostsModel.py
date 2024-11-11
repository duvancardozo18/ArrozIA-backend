from sqlalchemy import Column, Integer, Float
from src.database.database import Base
from sqlalchemy.orm import relationship  # Asegúrate de importar relationship

class AdditionalCosts(Base):
    __tablename__ = "costos_adicionales"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    costo_capacitacion_real = Column(Float, nullable=True)  # Costo capacitación real
    costo_control_roedores_real = Column(Float, nullable=True)  # Costo control de roedores real
    costo_capacitacion_estimado = Column(Float, nullable=True)  # Costo capacitación estimado
    costo_control_roedores_estimado = Column(Float, nullable=True)  # Costo control de roedores estimado

    # Relación con VariableCost
    gastos_variables = relationship("VariableCost", back_populates="costos_adicionales")

    def __repr__(self):
        return f"<AdditionalCosts(id={self.id}, costo_capacitacion_real={self.costo_capacitacion_real}, costo_control_roedores_real={self.costo_control_roedores_real}, costo_capacitacion_estimado={self.costo_capacitacion_estimado}, costo_control_roedores_estimado={self.costo_control_roedores_estimado})>"
