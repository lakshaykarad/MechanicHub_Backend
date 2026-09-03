from fastapi import FastAPI, status, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ....app import schemas
from ..database import get_db
from ..models import Mechanic

router = APIRouter(prefix="/mechanics",tags=["mechanics"],)

@router.get("", response_model=list[schemas.MechanicListResponse],status_code=status.HTTP_200_OK)
def list_mechanics(db : Session = Depends(get_db)):
    try:
        mechanic = db.query(Mechanic).all()
        return mechanic
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= "Database error while fetching mechanics"
        ) 
         

@router.get("/{mechanic_id}", response_model=schemas.MechanicDetailResponse, status_code=status.HTTP_200_OK)
def get_getmachanics(mechanic_id : int, db : Session = Depends(get_db)):
    try:
        mechanic = db.query(Mechanic).filter(Mechanic.id == mechanic_id).first()
        if not mechanic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )
        return mechanic
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    