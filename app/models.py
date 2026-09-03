from sqlalchemy import (Boolean,Column,Float,ForeignKey,Integer,String,Text,)
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from .database import Base
 
class Mechanic(Base):
    __tablename__ = "mechanics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    # it help when we will add google map apis. 
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    location_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    available_services = Column(JSON, nullable=False)  # list of strings
    working_hours = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    is_open = Column(Boolean, default=True, nullable=False)
    # use it for future.  

    service_requests = relationship(
        "ServiceRequest",  
        back_populates="mechanic", # sync with other table  
    )

class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    vehicle_number = Column(String, nullable=False)
    selected_service = Column(String, nullable=False)
    problem_description = Column(Text, nullable=False)
    mechanic_id = Column(Integer, ForeignKey("mechanics.id"), nullable=False)

    mechanic = relationship("Mechanic", back_populates="service_requests")
    
