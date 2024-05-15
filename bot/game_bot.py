from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from bot.games.guess_number import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


router_game = Router()
USER_ANSWER = ['y', 'yes', 'да', 'давай', 'играем', 'сыграем', 'ok', 'ок', 'хорошо']
NEGATIVE_ANSWER = ['n', 'no', 'нет', 'не', 'не хочу']


class myFSMState(StatesGroup):
    state_game = State()


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
    if not config_game['in_game']:
        fill_config()
        await state.update_data(name=message.text)
        await message.answer(text='Я загадал число от 1 до 100. Угадай какое!')
    else:
        await message.answer(text='Нужно писать числа от 1 до 100 или команды')


@router_game.message(StateFilter(myFSMState.state_game), F.text.lower().in_(NEGATIVE_ANSWER))
async def get_negative_answer(message: Message, state: FSMContext):
    if not config_game['in_game']:
        await state.clear()
        await message.answer(text='Захочешь поиграть, напиши')
    else:
        await message.answer(text='Нужно писать числа от 1 до 100 или команды')


def compare_condition(message: Message):
    num = message.text
    return num and num.isdigit() and 1 <= int(num) <= 100


@router_game.message(StateFilter(myFSMState.state_game), compare_condition)
async def process_game(message: Message, state: FSMContext):
    if config_game['in_game']:
        await state.update_data(name=message.text)
        answer = compare_answer(int(message.text))
        await message.answer(answer)
        if not config_game['in_game']:
            await state.clear()
            await message.answer(f'{get_user_stat()}\nСыграть еще /game')
    else:
        await message.answer(text='Мы еще не играем.')


router_game.message.register(get_rule, Command('rule'))
router_game.message.register(get_stat, Command('stat'))
