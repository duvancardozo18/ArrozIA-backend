# src/models/estadoModel.py
from sqlalchemy import Column, Integer, String
from src.database.database import Base
from sqlalchemy.orm import relationship

class Estado(Base):
    __tablename__ = "estado"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)

     # Relación hacia Task
    tasks = relationship("Task", back_populates="estado")