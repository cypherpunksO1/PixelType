from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from core.db.mixins import SerializerMixin

Base = declarative_base()


class Post(Base, SerializerMixin):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    key = Column(String)
    author = Column(String)
    title = Column(String)
    text = Column(String)
    views = Column(Integer, default=0)

    created = Column(Integer)
