import requests
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot.games import guess_number as gn
from bot import utils


router_game = Router(name='game')
USER_ANSWER = ['y', 'yes', 'да', 'давай', 'играем', 'сыграем', 'ok', 'ок', 'хорошо']
NEGATIVE_ANSWER = ['n', 'no', 'нет', 'не', 'не хочу']
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'


class myFSMState(StatesGroup):
    state_game = State()


async def invite_game(message: Message, state: FSMContext):
    await message.answer(gn.DESCRIPTION +
                         'Сыграем? (y/n)')
    utils.users_games.setdefault(message.from_user.id, gn.get_config_game())
    await state.set_state(myFSMState.state_game)


async def get_rule(message: Message):
    await message.answer(gn.RULE)


async def get_stat(message: Message):
    data = utils.users_games[message.from_user.id]
    await message.answer(gn.get_user_stat(data))


@router_game.message(Command('cancel'), StateFilter(myFSMState.state_game))
async def end_game(message: Message, state: FSMContext):
    id = message.from_user.id
    utils.users_games[id].update(gn.exit_game())
    await message.answer('Вы закончили игру')
    await state.clear()


@router_game.message(StateFilter(myFSMState.state_game),
                     F.text.lower().in_(USER_ANSWER))
async def get_game(message: Message, state: FSMContext):
    id = message.from_user.id
    if not utils.users_games[id]['in_game']:
        utils.users_games[id].update(gn.fill_config())
        await state.update_data(name=message.text)
        await message.answer(text='Я загадал число от 1 до 100. Угадай какое!')
    else:
        await message.answer(text='Пиши числа от 1 до 100 или команды')


@router_game.message(StateFilter(myFSMState.state_game),
                     F.text.lower().in_(NEGATIVE_ANSWER))
async def get_negative_answer(message: Message, state: FSMContext):
    if not utils.users_games[message.from_user.id]['in_game']:
        await state.clear()
        await message.answer(text='Захочешь поиграть, напиши')
    else:
        await message.answer(text='Нужно писать числа от 1 до 100 или команды')


@router_game.message(StateFilter(myFSMState.state_game),
                     lambda msg: utils.compare_condition(msg.text))
async def process_game(message: Message, state: FSMContext):
    if utils.users_games[message.from_user.id]['in_game']:
        id = message.from_user.id
        await state.update_data(name=message.text)
        num = int(message.text)
        if utils.users_games[id]['my_number'] == num:
            utils.users_games[id]['in_game'] = False
            utils.users_games[id]['total'] += 1
            utils.users_games[id]['wins'] += 1
            await message.answer('Вы угадали!!!')
            cat_response = requests.get(API_CATS_URL)
            if cat_response.status_code == 200:
                img = cat_response.json()[0]['url']
                await message.answer(img)
            await message.answer(f'{gn.get_user_stat(utils.users_games[id])}\n\n'
                                 f'Играем дальше... Угадывай!')
            utils.users_games[id].update(gn.fill_config())
        elif utils.users_games[id]['my_number'] < num:
            utils.users_games[id]['attempts'] -= 1
            await message.answer('Меньше')
        elif utils.users_games[id]['my_number'] > num:
            utils.users_games[id]['attempts'] -= 1
            await message.answer('Больше')

        if utils.users_games[id]['attempts'] == 0:
            utils.users_games[id]['in_game'] = False
            utils.users_games[id]['total'] += 1
            await message.answer('Попытки закончились.\n'
                                 'Загаданное число было ' \
                                 f'{utils.users_games[id]["my_number"]}\n'
                                 'Играем еще раз?')
    else:
        await message.answer(text='Мы еще не играем.')


router_game.message.register(get_rule, Command('rule'))
router_game.message.register(get_stat, Command('stat'))
