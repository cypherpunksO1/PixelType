from fastapi import APIRouter, UploadFile, File
import service.posts
import settings
from core.db.database import session
from models.db_models import Post
import time
import uuid
from models import pydantic_models

router = APIRouter()


@router.post('/post/create')
async def create_post(post: pydantic_models.Post):
    key = service.posts.make_post_key(post.title)

    if not post.author:
        post.author = 'Anonymously'

    # Convert Markdown to HTML, replace \n to <br> and add <a> to <h1>
    post.text = service.posts.convert_markdown_to_html(post.text)

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


@router.post("/image/upload")
async def create_upload_files(image: UploadFile = File()):
    file_extension = image.filename.split('.')[-1]
    file_location = f"{settings.MEDIA_DIR}/{uuid.uuid4()}.{file_extension}"

    with open(file_location, "wb+") as file_object:
        file_object.write(image.file.read())

    return {"image": image,
            'key': file_location}
