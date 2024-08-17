from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.database.database import Base 
import datetime 

class User(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key = True)
    nombre = Column(String(50), nullable=False )
    apellido = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(100),nullable=False)

class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer)
    access_toke = Column(String(450), primary_key=True)
    refresh_toke = Column(String(450),nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)


    #Modelo temporal para Roles------------------------------------
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    permissions = relationship("Permission", back_populates="role")

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship("Role", back_populates="permissions")