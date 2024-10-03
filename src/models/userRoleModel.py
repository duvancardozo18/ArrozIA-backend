from sqlalchemy import Column, Integer, ForeignKey
from src.database.database import Base

class UserRole(Base):
    __tablename__ = "usuario_rol"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    rol_id = Column(Integer, ForeignKey('rol.id'), nullable=False)
