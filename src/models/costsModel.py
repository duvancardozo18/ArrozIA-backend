from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base

class Costs(Base):
    __tablename__ = "gastos"

    id = Column(Integer, primary_key=True, index=True)
    cultivo_id = Column(Integer, ForeignKey("cultivo.id"), nullable=False)
    concepto = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    precio = Column(Float, nullable=False)

    cultivo = relationship("Crop", back_populates="gastos")
