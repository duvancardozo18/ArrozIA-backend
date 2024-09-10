import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from src.database.database import Base


class User(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key = True)
    nombre = Column(String(50), nullable=False )
    apellido = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(100),nullable=False)
    primer_login = Column(Boolean, default=True)

class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer)
    access_toke = Column(String(450), primary_key=True)
    refresh_toke = Column(String(450),nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)