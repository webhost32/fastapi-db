from datetime import datetime

from sqlalchemy.orm import Session
from app.database import models


def set_data(db: Session):
    data = models.Test(id=1, data=str(datetime.now()))
    db.add(data)
    db.commit()


def get_data(db: Session):
    return db.query(models.Test).all()
