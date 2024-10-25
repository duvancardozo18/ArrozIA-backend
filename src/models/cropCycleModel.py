from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base

class CropCycle(Base):
    __tablename__ = "crop_cycle"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)
    cultivo_id = Column(Integer, ForeignKey("cultivo.id"), nullable=False)
    
    # Relaciones
    cultivo = relationship("Cultivo", back_populates="crop_cycles")
