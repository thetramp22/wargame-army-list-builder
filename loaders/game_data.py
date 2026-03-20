from models.game import Game
from models.faction import Faction
from models.unit import Unit, ModelComposition
from models.model import Model


class GameData:
    def __init__(self):
        self.games_by_id: dict[str, Game] = {}
        self.factions_by_id: dict[str, Faction] = {}
        self.units_by_id: dict[str, Unit] = {}
        self.models_by_id: dict[str, Model] = {}
        self.models_by_unit: dict[str, list] = {}
        self.units_by_faction: dict[str, list] = {}
        self.factions_by_game: dict[str, list] = {}

    def get_game(self, game_id):
        return self.games_by_id[game_id]

    def get_faction(self, faction_id):
        return self.factions_by_id[faction_id]

    def get_unit(self, unit_id):
        return self.units_by_id[unit_id]

    def get_model(self, model_id):
        return self.models_by_id[model_id]

    def get_models_by_unit(self, unit_id):
        models = []
        for model in self.models_by_unit[unit_id]:
            models.append(self.models_by_id[model])
        return models

    def get_units_by_faction(self, faction_id):
        units = []
        for unit in self.units_by_faction[faction_id]:
            units.append(unit)
        return units

    def get_factions_by_game(self, game_id):
        factions = []
        for faction in self.factions_by_game[game_id]:
            factions.append(faction)
        return factions
