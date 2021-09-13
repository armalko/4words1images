import pickle
from random import choice, shuffle
import pathlib

import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)


class Game:
    with open(str(pathlib.Path().resolve()) + '/tg_bot/game_utils/games.pickle', 'rb') as file:
        game_list = pickle.load(file)
        logging.info('Pictures have been loaded to RAM')

    @staticmethod
    def find_game_by_id(game_id: int):
        return Game.game_list[game_id]

    @staticmethod
    def get_random_game():
        return choice(Game.game_list)

    @staticmethod
    def get_ready_to_send_text(game: Dict):
        letters_list = [s for s in game['answer']]
        for i in range(12 - len(letters_list)):
            letters_list.append(choice(''.join([chr(i) for i in range(ord('А'), ord('А')+32)])))

        shuffle(letters_list)

        return f"Слово состоит из {len(game['answer'])} букв\n" \
               f"Буквы:\n{'  '.join(letters_list[:6])}\n{'  '.join(letters_list[6:])}"
