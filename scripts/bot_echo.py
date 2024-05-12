#!/usr/bin/env python3
from dotenv import load_dotenv
from os import getenv
from aiogram import Bot
from aiogram import Dispatcher
from bot import echo_bot, game_bot


load_dotenv()
mybot = Bot(token=getenv('TOKEN'))
DISPATCHER = Dispatcher()


def main():
    DISPATCHER.include_router(echo_bot.router)
    DISPATCHER.include_router(game_bot.router_game)


if __name__ == '__main__':
    main()
    DISPATCHER.run_polling(mybot)
