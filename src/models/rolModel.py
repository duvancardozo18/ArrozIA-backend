from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.database.database import Base


class Rol(Base):
    __tablename__ = 'rol'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(255))

    # Relación con Permission usando la tabla intermedia rol_permiso
    permissions = relationship("Permission", secondary="rol_permiso", back_populates="roles")
