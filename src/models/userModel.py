from sqlalchemy import Boolean, Column, Integer, String
from src.database.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key = True)
    nombre = Column(String(50), nullable=False )
    apellido = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(100),nullable=False)
    primer_login = Column(Boolean, default=True)
    
    
    #Relación con task
    tasks = relationship("Task", back_populates="usuario")  # Nueva relación