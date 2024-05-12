from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType


DISPATCHER = Dispatcher()


@DISPATCHER.message(Command('start'))
async def start_bot(message: Message):
    name = message.from_user.full_name
    await message.answer(f'Привет!\nНапиши мне что-нибудь {name}')


@DISPATCHER.message(Command('help'))
async def help_bot(message: Message):
    await message.answer('Напиши мне что-нибудь')


async def send_bot(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Данный тип сообщения не поддерживается')


async def send_photo(message: Message):
    await message.reply_photo(message.photo[0].file_id)


async def send_sticker(message: Message):
    await message.reply(text='И я так могу...')
    await message.answer_sticker(message.sticker.file_id)


async def send_anima(message: Message):
    await message.reply(text='И у меня такая есть...')
    await message.answer_animation(message.animation.file_id)


DISPATCHER.message.register(send_photo, F.photo)
DISPATCHER.message.register(send_sticker, F.sticker)
DISPATCHER.message.register(send_anima, F.animation)
DISPATCHER.message.register(send_bot)