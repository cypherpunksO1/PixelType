from aiogram.types import Message
from aiogram.types import (FSInputFile, 
                           InlineKeyboardButton, 
                           InlineKeyboardMarkup)
from aiogram.filters import (Command, 
                             CommandStart)
from aiogram.fsm.context import FSMContext
from aiogram import F, Router

import asyncio, os

from core.services.posts_service import post_service
from core.conf.bot import bot
from core.schemas import PostScheme


messages_router = Router(name="messages")


@messages_router.message(CommandStart())
async def start_arg_message(msg: Message):
    answer = "Hello!"
    await msg.answer(text=answer)
    
    
@messages_router.message()
async def create_post(msg: Message):
    text: str = msg.html_text
    
    try:
        title = text.split("\n", maxsplit=1)[0]
        text = text.split("\n", maxsplit=1)[1:][0]

        post = PostScheme(
            title=title, 
            author=msg.from_user.first_name, 
            text=text
        )
        post_key = post_service.create_post(post=post)
        
        url = "https://pixeltype.egoryolkin.ru/type/" + post_key
        
        reply_markup =InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Читать 👀", 
                                        url=url)
            ]
        ])
        await msg.answer(text=title, 
                        reply_markup=reply_markup)
    except IndexError:
        answer = "Пример использования.\n\nЗаголовок поста\nТекст поста"
        await msg.answer(text=answer)
