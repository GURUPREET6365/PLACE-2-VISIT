from .database import Base
from sqlalchemy import Column, Integer, String, DateTime
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

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False , index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default="user")
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    places = relationship("Place", back_populates="user")
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )