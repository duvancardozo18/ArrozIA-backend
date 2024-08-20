from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base 

class UsuarioFincaRol(Base):
    __tablename__ = 'usuario_finca'
    
    usuario_id = Column(Integer, ForeignKey('usuario.id'), primary_key=True)
    rol_id = Column(Integer, ForeignKey('rol.id'), primary_key=True)
    finca_id = Column(Integer, primary_key=True)

class Rol(Base):
    __tablename__ = 'rol'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(255))
