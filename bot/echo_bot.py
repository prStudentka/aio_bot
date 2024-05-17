from aiogram import Router, F
from aiogram.filters import Command, StateFilter, CommandStart
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from bot import game_bot


router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def start_bot(message: Message):
    name = message.from_user.full_name
    await message.answer(f'Привет!\nНапиши мне что-нибудь {name}')


@router.message(Command('help'))
async def help_bot(message: Message):
    await message.answer('Напиши мне что-нибудь.\n'
                         'Хочешь со мной поиграть напиши команду /game')


@router.message(Command('game'))
async def get_game(message: Message, state: FSMContext):
    await game_bot.invite_game(message, state)


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


router.message.register(send_photo, F.photo)
router.message.register(send_sticker, F.sticker)
router.message.register(send_anima, F.animation)
router.message.register(send_bot, StateFilter(default_state))
