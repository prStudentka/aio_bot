users_games = {}


def compare_condition(msg):
    return msg and msg.isdigit() and 1 <= int(msg) <= 100