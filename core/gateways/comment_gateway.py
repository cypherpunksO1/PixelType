from sqlalchemy import exc

from core.conf.database import session, Session

from core import exceptions
from core import aliases
from core.gateways.abstract_gateway import AbstractGateway
from core.models import Comment


class CommentGateway(AbstractGateway):
    def __init__(self, 
                 session: Session):
        self.session = session

    def get(self, pk: int) -> Comment:
        return self.session.query(Comment).get(pk)
    
    def get_all(self) -> list[Comment]:
        return self.session.query(Comment).all()
    
    def filter_by(self, **kwargs) -> list[Comment]:
        return self.session.query(Comment).filter_by(**kwargs).all()


    def create(self, comment: Comment):
        self.session.add(comment)
        self.session.commit()

    def update(self, pk: int, comment: Comment):
        for key, value in comment.to_dict().items():
            setattr(comment, key, value)
            
        self.session.commit()

    def delete(self, pk):
        self.session.query(Comment).filter(Comment.pk == pk).delete()
        self.session.commit()


comment_gateway = CommentGateway(session=session)