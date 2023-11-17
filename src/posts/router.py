from fastapi import APIRouter
from fastapi import (UploadFile, 
                     File)

from core.conf.config import MEDIA_DIR

from core.services.posts_service import post_service
from core.schemas import *

import uuid

posts_router = APIRouter()


@posts_router.post('/create', 
                   response_model=PostResponseSchema)
async def create_post(post: PostScheme):
    post_key = post_service.create_post(post=post)

    return PostResponseSchema(
        key=post_key
    )


@posts_router.post("/image/upload", 
                   response_model=ImageResponseSchema)
async def create_upload_files(image: UploadFile = File()):
    file_extension = image.filename.split('.')[-1]
    file_location = f"{MEDIA_DIR}/{uuid.uuid4()}.{file_extension}"

    with open(file_location, "wb+") as file_object:
        file_object.write(image.file.read())

    return ImageResponseSchema(
        image=image, 
        path=file_location
    )
