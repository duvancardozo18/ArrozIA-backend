from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timedelta
from src.database.database import Base

class PasswordReset(Base):
    __tablename__ = 'password_resets'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def is_token_expired(self):
        expiration_time = self.created_at + timedelta(hours=1)
        return datetime.utcnow() > expiration_time
