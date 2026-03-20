from models.game import Game
from models.faction import Faction
from models.unit import Unit, ModelComposition
from models.model import Model
from loaders.game_data import GameData
import json
import sys

filepath = "./data/units.json"


class DataLoader:
    def __init__(self):
        self._data = {}
        self._game_data = GameData()

    def load(self):
        self._get_data()
        self._load_games()
        self._load_factions()
        self._load_models()
        self._load_units()
        return self._game_data

    def _get_data(self):
        try:
            with open(filepath, "r") as file:
                data = json.load(file)
                self._data = data

        except FileNotFoundError:
            print(f"Error: The file '{filepath}' was not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(
                f"Error: Failed to decode JSON from the file '{filepath}'. The file may be malformed."
            )
            sys.exit(1)

    def _load_games(self):
        for game in self._data["games"]:
            key = game["game_id"]
            self._game_data.games_by_id[key] = Game(game["game_id"], game["game_name"])

    def _load_factions(self):
        for faction in self._data["factions"]:
            key = faction["faction_id"]
            self._game_data.factions_by_id[key] = Faction(
                faction["faction_id"], faction["faction_name"], faction["game_id"]
            )
            if faction["game_id"] in self._game_data.factions_by_game:
                self._game_data.factions_by_game[faction["game_id"]].append(
                    faction["faction_id"]
                )
            else:
                self._game_data.factions_by_game[faction["game_id"]] = [
                    faction["faction_id"]
                ]

    def _load_models(self):
        for model in self._data["models"]:
            key = model["model_id"]
            self._game_data.models_by_id[key] = Model(
                model["model_id"], model["model_name"]
            )

    def _load_units(self):
        for unit in self._data["units"]:
            key = unit["unit_id"]
            faction_obj = self._game_data.factions_by_id[unit["faction_id"]]
            models = []
            for model in unit["models"]:
                models.append(
                    ModelComposition(
                        self._game_data.models_by_id[model["model_id"]],
                        model["min_quantity"],
                        model["max_quantity"],
                    )
                )
                if unit["unit_id"] in self._game_data.models_by_unit:
                    self._game_data.models_by_unit[unit["unit_id"]].append(
                        model["model_id"]
                    )
                else:
                    self._game_data.models_by_unit[unit["unit_id"]] = [
                        model["model_id"]
                    ]
            self._game_data.units_by_id[key] = Unit(
                unit["unit_id"],
                unit["unit_name"],
                faction_obj,
                unit["base_points"],
                unit["role"],
                unit["keywords"],
                models,
            )
            if unit["faction_id"] in self._game_data.units_by_faction:
                self._game_data.units_by_faction[unit["faction_id"]].append(
                    unit["unit_id"]
                )
            else:
                self._game_data.units_by_faction[unit["faction_id"]] = [unit["unit_id"]]
