from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.database import Base

class WeightUnit(Base):
    __tablename__ = 'unidad_peso'

    id = Column(Integer, primary_key=True, autoincrement=True)
    unit = Column(String(50), nullable=False)

    # Inverse relationship
    crops = relationship("Crop", order_by="Crop.id", back_populates="weightUnit")
