from sqlalchemy import Column, Integer, String, Text, Float
from src.database.database import Base

class LaborCultural(Base):
    __tablename__ = 'labor_cultural'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio_hora_real = Column(Float, nullable=True)  # Precio por hora real
    precio_hora_estimado = Column(Float, nullable=True)  # Precio por hora estimado

    def __repr__(self):
        return f"<LaborCultural(id={self.id}, nombre={self.nombre}, precio_hora_real={self.precio_hora_real}, precio_hora_estimado={self.precio_hora_estimado})>"
