from sqlalchemy import Column, ForeignKey, Integer, String

from src.database.database import Base


class UserFarmRol(Base):
    __tablename__ = 'usuario_finca'
    
    usuario_id = Column(Integer, ForeignKey('usuario.id'), primary_key=True)
    rol_id = Column(Integer, ForeignKey('rol.id'), primary_key=True)
    finca_id = Column(Integer, primary_key=True)
