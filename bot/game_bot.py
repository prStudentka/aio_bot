from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from bot.games.guess_number import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


router_game = Router()
USER_ANSWER = ['y', 'yes', 'да', 'давай', 'играем', 'сыграем', 'ok', 'ок', 'хорошо']


class myFSMState(StatesGroup):
    state_game = State()
    state_echo = State()


async def invite_game(message: Message, state: FSMContext):
    await message.answer('Игра "Угадай число".\n'
                         'Правила игры - отправь команду /rule \n'
                         'Выйти из игры - команда /cancel\n'
                         'Посмотреть статистику - команда /stat\n'
                         'Сыграем? (y/n)')
    await state.set_state(myFSMState.state_game)


async def get_rule(message: Message):
    await message.answer(RULE)


async def get_stat(message: Message):
    await message.answer(get_user_stat())


@router_game.message(Command('cancel'), StateFilter(myFSMState.state_game))
async def end_game(message: Message, state: FSMContext):
    await message.answer('Вы закончили игру')
    await state.clear()


@router_game.message(StateFilter(myFSMState.state_game), F.text.lower().in_(USER_ANSWER))
async def get_game(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text='Фигня какая-то')


router_game.message.register(get_rule, Command('rule'))
router_game.message.register(get_stat, Command('stat'))
