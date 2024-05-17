import random


ATTEMPTS = 5
DESCRIPTION = '''Игра "Угадай число".\n
                 Правила игры - отправь команду /rule \n
                 Выйти из игры - команда /cancel\n
                 Посмотреть статистику - команда /stat\n
              '''

RULE = f'''Правила игры:\n
        Я загадываю число 1 до 100,\n
        а Вам надо его угадать.\n
        У вас {ATTEMPTS} попыток.'''


def get_config_game():
    return {'in_game': False,
            'my_number': None,
            'total': 0,
            'wins': 0,
            'attempts': None
            }


def fill_config():
    return {'in_game': True,
            'my_number': random.randint(1, 100),
            'attempts': ATTEMPTS
            }


def exit_game():
    return {'in_game': False,
            'my_number': None,
            'attempts': None
           }


def get_user_stat(data):
    return f'Игр сыграно: {data["total"]}\nВыигрышей: {data["wins"]}'

