# src/models/estadoModel.py
from sqlalchemy import Column, Integer, String
from src.database.database import Base

class Estado(Base):
    __tablename__ = "estado"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
