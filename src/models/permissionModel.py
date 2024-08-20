from sqlalchemy import Column, Integer, String, ForeignKey
from src.database.database import Base

class Permiso(Base):
    __tablename__ = 'permiso'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(255))

class RolPermiso(Base):
    __tablename__ = 'rol_permiso'
    
    rol_id = Column(Integer, ForeignKey('rol.id'), primary_key=True)
    permiso_id = Column(Integer, ForeignKey('permiso.id'), primary_key=True)
