from fastapi import FastAPI, Request, Response, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.database import engine, SessionLocal
from app.database import models, crud
from app.dependencies import get_settings, get_db

settings = get_settings()
app = FastAPI(title="Test-db")


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.get("/")
async def get_data(db: Session = Depends(get_db)):
    return crud.get_data(db)


@app.get("/ping")
async def ping():
    return "pong"


@app.on_event("startup")
async def startup():
    models.DataBase.metadata.create_all(bind=engine)
    with Session(engine) as db:
        try:
            crud.set_data(db)
        except IntegrityError:
            pass
