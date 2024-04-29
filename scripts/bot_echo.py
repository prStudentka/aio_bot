#!/usr/bin/env python3
from dotenv import load_dotenv
from os import getenv
from aiogram import Bot
from echo_bot import DISPATCHER


load_dotenv()
mybot = Bot(token=getenv('TOKEN'))


if __name__ == '__main__':
    DISPATCHER.run_polling(mybot)
