from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float
from src.database.database import Base

class FinancialExpenses(Base):
    __tablename__ = "gastos_administrativos_financieros"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    costo_impuestos_real = Column(Float, nullable=True)  # Costo impuestos real
    costo_impuestos_estimado = Column(Float, nullable=True)  # Costo impuestos estimado
    costo_seguros_real = Column(Float, nullable=True)  # Costo seguros real
    costo_seguros_estimado = Column(Float, nullable=True)  # Costo seguros estimado

    # Relación con VariableCost
    gastos_variables = relationship("VariableCost", back_populates="gastos_administrativos_financieros")

    def __repr__(self):
        return f"<FinancialExpenses(id={self.id}, costo_impuestos_real={self.costo_impuestos_real}, costo_impuestos_estimado={self.costo_impuestos_estimado}, costo_seguros_real={self.costo_seguros_real}, costo_seguros_estimado={self.costo_seguros_estimado})>"
