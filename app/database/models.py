from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# This is the table for the places.
class Place(Base):
    __tablename__ = 'places'
    
    id = Column(Integer, primary_key=True, nullable=False , index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    place_name = Column(String, nullable=False)
    place_address = Column(String, nullable=False)
    user = relationship("User", back_populates="places")
    pincode = Column(Integer, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class Votes(Base):
    __tablename__ = 'votes'
    
    id = Column(Integer, primary_key=True, nullable=False , index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    place_id = Column(Integer, ForeignKey("places.id", ondelete="CASCADE"), nullable=False)

    vote= Column(Boolean, nullable=True)

    user = relationship("User", back_populates="votes")

    voted_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False , index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    role = Column(String, nullable=False, server_default="user")
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=True)
    provider = Column(String, nullable=False, server_default='local')
    google_sub = Column(String, unique=True, nullable=True)
    places = relationship("Place", back_populates="user")
    votes = relationship("Votes", back_populates="user")
    profile_url = Column(String, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

