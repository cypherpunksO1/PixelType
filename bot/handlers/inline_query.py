from aiogram.types import (InlineQuery, 
                           InlineQueryResultArticle, 
                           InputTextMessageContent)
from aiogram.types import (InlineKeyboardButton, 
                           InlineKeyboardMarkup)
from aiogram import F, Router

from core.services.posts_service import post_service
from core.conf.bot import bot
from core.conf import config
from core.schemas import PostScheme

inline_router = Router(name="inline")


@inline_router.inline_query()
async def inline_handler(query: InlineQuery):
    text: str = query.query
    
    try:
        title = text.split("\n", maxsplit=1)[0]
        text = text.split("\n", maxsplit=1)[1:][0]
        
        if text.endswith("/end"):
            post = PostScheme(
                title=title, 
                author=query.from_user.first_name, 
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
            
            results = [
                InlineQueryResultArticle(
                    id="1", 
                    title=title, 
                    description=text, 
                    input_message_content=InputTextMessageContent(
                        message_text=f"<b>{title}</b>", 
                        parse_mode="HTML"
                    ), 
                    reply_markup=reply_markup
                )
            ]

            await query.answer(results, cache_time=1)
    except IndexError:
        pass
    