import logging
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import Mechanic

from .mechanics import SEED_MECHANICS

# it help to ganrate the log message where tag is __name__
logger = logging.getLogger(__name__)

def seed_data() -> None: 
    Base.metadata.create_all(bind=engine)
    db : Session = SessionLocal()
    
    try:
        if db.query(Mechanic).first():
            logger.info("Database already contains mechanics – skipping seed.")
            return 
        for machanic_data in SEED_MECHANICS:
            mechanic = Mechanic(**machanic_data) # no need to make key and value ** can read all the things in once 
            db.add(mechanic)
        
        db.commit()

    except:
        db.rollback()
        raise
    finally:
        db.close()
        