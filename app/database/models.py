from sqlalchemy import Column, Integer, Text

from app.database.database import DataBase


class Test(DataBase):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    data = Column(Text)
