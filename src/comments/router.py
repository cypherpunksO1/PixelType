from fastapi import APIRouter, Response
from fastapi import (UploadFile, 
                     File)

from core.conf.config import MEDIA_DIR

from core.services.comments_service import comment_service
from core.schemas import *

import uuid

comments_router = APIRouter()


@comments_router.post('/create')
async def create_post(comment: CommentScheme):
    post_key = comment_service.create_comment(comment=comment)

    return Response(
        status_code=201
    )


@comments_router.get('/get/{post_key}/')
async def create_post(post_key: str):
    comments = comment_service.get_comments(post_key=post_key)
    comments.reverse()
    return comments