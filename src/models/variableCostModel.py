from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base
from src.models.financialExpensesModel import FinancialExpenses  # IMPORTANTE: Importa correctamente FinancialExpenses
from src.models.waterModel import Agua  # Asegúrate de importar correctamente

class VariableCost(Base):
    __tablename__ = 'gastos_variables'

    id = Column(Integer, primary_key=True, index=True)
    id_costos_adicionales = Column(Integer, ForeignKey('costos_adicionales.id'))
    id_agua = Column(Integer, ForeignKey('agua.id'))  # Correcta referencia a la tabla 'agua'
    id_gastos_administrativos_financieros = Column(Integer, ForeignKey('gastos_administrativos_financieros.id'))
    descripcion = Column(String)

    # Relaciones con otras tablas
    costos_adicionales = relationship("AdditionalCosts", back_populates="gastos_variables")
    agua = relationship("Agua", back_populates="gastos_variables")
    gastos_administrativos_financieros = relationship("FinancialExpenses", back_populates="gastos_variables")
