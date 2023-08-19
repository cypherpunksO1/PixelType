from pydantic import BaseModel


class Post(BaseModel):
    title: str
    author: str
    text: str
