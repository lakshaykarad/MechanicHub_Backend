from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class MechanicBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    rating: float = Field(..., ge=0, le=5, examples=[4.5])
    latitude: float = Field(..., ge=-90, le=90, examples=[28.4595])
    longitude: float = Field(..., ge=-180, le=180, examples=[77.0266])
    location_name: str = Field(..., min_length=2, max_length=50, examples=["Sector 29"])
    address: str = Field(..., min_length=5, max_length=200, examples=["Shop 12, Main Market, Sector 29"])
    available_services: List[str] = Field(..., min_length=1)
    working_hours: str = Field(..., examples=["Mon-Sat: 9:00 AM - 8:00 PM"])
    phone_number: str = Field(..., pattern=r"^\+?[0-9 -]{10,15}$")
    is_open: bool = Field(..., examples=[True])

class MechanicListResponse(BaseModel):
    """Response model for Home Screen – minimal fields."""
    id: int
    name: str
    rating: float
    location_name: str
    is_open: bool 

class MechanicDetailResponse(MechanicBase):
    """Full mechanic details."""
    id: int
 
class ServiceRequestCreate(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    phone_number: str = Field(
        ...,
        pattern=r"^\+?[0-9]{10,15}$",
        examples=["+91-9876543210"],
    )
    
    vehicle_number: str = Field(..., min_length=6, max_length=15)
    selected_service: str = Field(..., min_length=2, max_length=100)
    problem_description: str = Field(..., min_length=10, max_length=500)
    mechanic_id: int = Field(..., gt=0)

    @field_validator("phone_number", mode="before")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = v.replace(" ", "").replace("-", "")
        if not v.startswith("+"):
            v = "+91" + v
        return v


class ServiceRequestResponse(BaseModel):
    message: str = Field(..., examples=["Service request submitted successfully"])
    request_id: int = Field(..., gt=0)