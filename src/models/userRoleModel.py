from sqlalchemy import Column, Integer, ForeignKey
from src.database.database import Base

class UserRole(Base):
    __tablename__ = "usuario_rol"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario_id"), nullable=False)
    rol_id = Column(Integer, ForeignKey("rol_id"), nullable=False)
