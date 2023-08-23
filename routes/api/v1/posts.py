from fastapi import APIRouter
from core.db.database import session
from sqlalchemy import func
from models.db_models import Post
import markdown
import utils
import time
from models import pydantic_models

posts_router = APIRouter()


@posts_router.post('/api/v1/post/create')
async def create_post(post: pydantic_models.Post):
    # Make key
    key = utils.transliterate_title(post.title)

    # If exists reply key - add exists reply keys count to end.
    if session.query(Post).filter(func.lower(Post.key).ilike(f"%{key.lower()}%")).count() > 0:
        key = '%s-%s' % (key, session.query(Post).filter(func.lower(Post.key).ilike(f"%{key.lower()}%")).count() + 1)

    if not post.author:
        post.author = 'Anonymously'

    # Convert Markdown to HTML, replace \n to <br> and add <a> to <h1>
    post.text = utils.add_tag_to_title(
        markdown.markdown(post.text).replace('\n', '<br>')
    )

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
