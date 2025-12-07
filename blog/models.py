from sqlalchemy import Column , Integer , String
from .database import Base

"""defing every field to be inside the Table , Defing The Model Parameters"""

class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    body = Column(String)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True)
    user_name = Column(String)
    email = Column(String)
    password = Column(String)
