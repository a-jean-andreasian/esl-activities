from dataclasses import dataclass
import json
from threading import Lock


class EslGames:
    __filepath = 'games.json'

    @dataclass
    class Game:
        name: str
        description: str

        def __to_dict__(self):
            return {
                'name': self.name,
                'description': self.description
            }

    def __init__(self):
        self.games: list[dict[EslGames.Game]] = None
        self.lock = Lock()

    def load_games(self) -> dict:
        if not self.games:
            with self.lock:
                with open(self.__filepath, 'r', encoding='utf-8') as f:
                    self.games = json.load(f)
        return self.games

    def __save_games(self):
        with self.lock:
            with open(self.__filepath, 'w', encoding='utf-8') as f:
                json.dump(self.games, f, indent=4)

    @property
    def names(self):
        if not self.games:
            self.load_games()
        return [game['name'] for game in self.games]

    def add_game(self, name: str, description: str) -> None:
        if not self.games:
            self.load_games()

        if name not in self.names:
            game = self.Game(name=name, description=description).__to_dict__()
            self.games.append(game)
            self.__save_games()

        else:
            print("Game", name, "already exists.")

# {'name': 'Lie to Me', 'description': 'Students say three sentences about themselves. Two are true, one’s fake. Class interrogates them, then votes.'}
