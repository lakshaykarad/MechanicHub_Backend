from fastapi import FastAPI, status, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ....app import schemas
from ..database import get_db
from ..models import ServiceRequest, Mechanic


router = APIRouter(
    prefix="/service-requests",
    tags=["service requests"]
)


@router.post("", response_model=schemas.ServiceRequestResponse,status_code=status.HTTP_201_CREATED)
def create_service_request(request : schemas.ServiceRequestCreate, db : Session = Depends(get_db)):
    try:
        mechanic = db.query(Mechanic).filter(Mechanic.id == request.mechanic_id).first()
        if not mechanic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        
        db_request = ServiceRequest(
            customer_name=request.customer_name,
            phone_number=request.phone_number,
            vehicle_number=request.vehicle_number,
            selected_service=request.selected_service,
            problem_description=request.problem_description,
            mechanic_id=request.mechanic_id,
        )
        
        db.add(db_request)
        db.commit()
        db.refresh(db_request)
        
        return schemas.ServiceRequestResponse(message="Service request submitted successfully",request_id=db_request.id)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        