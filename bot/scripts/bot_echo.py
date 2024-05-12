#!/usr/bin/env python3
from dotenv import load_dotenv
from aiogram import Bot
from aiogram import Dispatcher
from bot import echo_bot, game_bot
from bot.config import TOKEN

load_dotenv()


def main():
    mybot = Bot(token=TOKEN)
    DISPATCHER = Dispatcher()
    DISPATCHER.include_router(echo_bot.router)
    DISPATCHER.include_router(game_bot.router_game)
    DISPATCHER.run_polling(mybot)


if __name__ == '__main__':
    main()

