from sqlalchemy import Column
from sqlalchemy import (Integer, 
                        String, 
                        DateTime)
from sqlalchemy.ext.declarative import declarative_base

from core.conf.database import Base, engine
from core.mixins import SerializerMixin

from datetime import datetime


class Post(Base, SerializerMixin):
    __tablename__ = 'post'

    pk = Column(Integer, primary_key=True)
    key = Column(String)
    author = Column(String)
    title = Column(String)
    text = Column(String)
    views = Column(Integer, default=0)

    created = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(engine)