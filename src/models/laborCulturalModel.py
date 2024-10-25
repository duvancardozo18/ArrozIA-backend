from sqlalchemy import Column, Integer, String, Text
from src.database.database import Base

class LaborCultural(Base):
    __tablename__ = 'labor_cultural'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
