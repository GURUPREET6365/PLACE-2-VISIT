from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import text

"""
creator_id = Column(
    Integer,
    ForeignKey("users.id", ondelete="SET NULL"),
    nullable=True
)

You are telling PostgreSQL:

If the referenced user row is deleted,
then instead of deleting this row,
set creator_id to NULL.
"""

# This is the table for the places.
class Place(Base):
    __tablename__ = 'places'
    
    id = Column(Integer, primary_key=True, nullable=False , index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    place_name = Column(String, nullable=False)
    about_place = Column(String, nullable=True)
    place_address = Column(String, nullable=False)
    user = relationship("User", back_populates="places")
    ratings = relationship("Ratings", back_populates="place")
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

class Ratings(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True, nullable=False , index=True)
    place_id = Column(Integer, ForeignKey("places.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    overall = Column(Integer, nullable=False)
    cleanliness = Column(Integer, nullable=False)
    safety = Column(Integer, nullable=False)
    crowd_behavior = Column(Integer, nullable=False)
    # This is the light at night like streetlight.
    lightning = Column(Integer, nullable=False)
    transport_access = Column(Integer, nullable=False)
    facility_quality = Column(Integer, nullable=False)
    user = relationship("User", back_populates="ratings")

    __table_args__ = (
        CheckConstraint("overall BETWEEN 1 AND 5"),
        CheckConstraint("cleanliness BETWEEN 1 AND 5"),
        CheckConstraint("safety BETWEEN 1 AND 5"),
        CheckConstraint("crowd_behavior BETWEEN 1 AND 5"),
        CheckConstraint("lightning BETWEEN 1 AND 5"),
        CheckConstraint("transport_access BETWEEN 1 AND 5"),
        CheckConstraint("facility_quality BETWEEN 1 AND 5"),
        UniqueConstraint("user_id", "place_id", name="unique_user_place_rating"),
    )

    place = relationship("Place", back_populates="ratings")
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    found_place = Column(Boolean, nullable=True)
    message = Column(String, nullable=False)