from fastapi import APIRouter
from core.db.database import session
from sqlalchemy import func
from models.db_models import Post
import utils
import time
from models import pydantic_models

posts_router = APIRouter()


@posts_router.post('/api/v1/post/create')
async def create_post(post: pydantic_models.Post):
    key = utils.transform_title(post.title)

    if session.query(Post).filter(func.lower(Post.key).ilike(f"%{key.lower()}%")).count() > 0:
        key = '%s-%s' % (key, session.query(Post).filter(func.lower(Post.key).ilike(f"%{key.lower()}%")).count() + 1)

    if not post.author:
        post.author = 'Anonymously'

    post.text = post.text.replace('\n', '<br>')

    post = Post(
        author=post.author,
        title=post.title,
        key=key,
        text=post.text,
        created=time.time()
    )
    session.add(post)
    session.commit()

    return {'key': post.key}


# @posts_router.get('/api/v1/posts/')
# async def create_post(limit: int = 10, offset: int = 0):
#     if limit >= 50:
#         limit = 50
#     queryset = session.query(Post).limit(limit).offset(offset)
#
#     return [_.to_dict() for _ in queryset]
