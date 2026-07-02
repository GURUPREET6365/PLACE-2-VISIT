from app.database.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app.routers.users.models import User



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
