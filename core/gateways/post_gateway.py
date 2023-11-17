from sqlalchemy import exc

from core.conf.database import session, Session

from core import exceptions
from core import aliases
from core.gateways.abstract_gateway import AbstractGateway
from core.models import Post


class PostGateway(AbstractGateway):
    def __init__(self, 
                 session: Session):
        self.session = session

    def get(self, pk: int) -> Post:
        return self.session.query(Post).get(pk)
    
    def get_all(self) -> list[Post]:
        return self.session.query(Post).all
    
    def filter_by(self, **kwargs) -> list[Post]:
        return self.session.query(Post).filter_by(**kwargs).all()


    def create(self, post: Post):
        try:
            self.session.add(post)
            self.session.commit()
        except exc.IntegrityError:
            self.session.rollback()
            raise exceptions.UserAlreadyExists()

    def update(self, pk: int, post: Post):
        for key, value in post.to_dict().items():
            setattr(post, key, value)
            
        self.session.commit()

    def delete(self, pk):
        self.session.query(Post).filter(Post.pk == pk).delete()
        self.session.commit()


post_gateway = PostGateway(session=session)