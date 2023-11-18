from aiogram.types import BotCommand

from bot.handlers.messages import messages_router 
from bot.handlers.inline_query import inline_router

from core.conf.bot import bot, dp

dp.include_routers(messages_router,
                   inline_router)


async def set_default_commands(dp):
    await bot.set_my_commands(
        [
            BotCommand(
                command='start', 
                description='Start bot'
            ),
        ]
    )


async def start(dispatcher) -> None:
    bot_name = dict(await bot.get_me()).get('username')
    await set_default_commands(dispatcher)
    print(f'#    start on @{bot_name}')


async def end(dispatcher) -> None:
    bot_name = dict(await bot.get_me()).get('username')
    print(f'#    end on @{bot_name}')


async def main():
    await start(dispatcher=dp)
    await dp.start_polling(bot)
    await end(dispatcher=dp)
    