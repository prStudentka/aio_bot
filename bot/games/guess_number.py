import random


ATTEMPTS = 5
RULE = f'''Правила игры:\n
        Я загадываю число 1 до 100,\n
        а Вам надо его угадать.\n
        У вас {ATTEMPTS} попыток.'''


config_game = { 'in_game': False,
                'my_number': None,
                'total': 0,
                'wins': 0,
                'attempts': None}


def fill_config():
    config_game['in_game'] = True
    config_game['my_number'] = random.randint(1, 100)
    config_game['attempts'] = ATTEMPTS


def get_user_stat():
    return f'Игр сыграно: {config_game["total"]}\nВыигрышей: {config_game["wins"]}'


def compare_answer(num):
    if config_game['attempts'] == 0:
        config_game['in_game'] = False
        config_game['total'] += 1
        return f'Попытки закончились. Загаданное число было {config_game["my_number"]}'

    if num == config_game['my_number']:
        config_game['in_game'] = False
        config_game['total'] += 1
        config_game['wins'] += 1
        return 'Вы угадали!!!'
    elif num > config_game['my_number']:
        config_game['attempts'] -= 1
        return 'Меньше'
    elif num < config_game['my_number']:
        config_game['attempts'] -= 1
        return 'Больше'

