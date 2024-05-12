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


def get_random():
    return random.randint(1, 100)


def get_user_stat():
    return f'Игр сыграно: {config_game["total"]}\nВыигрышей: {config_game["wins"]}'
