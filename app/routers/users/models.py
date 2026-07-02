from app.database.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False , index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    role = Column(String, default='user', nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=True)
    provider = Column(String, nullable=False, server_default='local')
    google_sub = Column(String, unique=True, nullable=True)
    places = relationship("Place", back_populates="user")
    votes = relationship("Votes", back_populates="user")
    ratings = relationship("Ratings", back_populates="user")
    profile_url = Column(String, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
