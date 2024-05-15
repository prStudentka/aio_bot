#!/usr/bin/env python3
from dotenv import load_dotenv
from aiogram import Bot
from aiogram import Dispatcher
from bot import echo_bot, game_bot
from bot.config import TOKEN

load_dotenv()


def main():
    mybot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(echo_bot.router)
    dp.include_router(game_bot.router_game)
    dp.run_polling(mybot)


if __name__ == '__main__':
    main()

