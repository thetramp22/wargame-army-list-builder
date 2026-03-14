from models.game import Game
from models.faction import Faction
from models.unit import Unit, ModelComposition
from models.model import Model
import json
import sys

filepath = "./data/units.json"

class DataLoader():
  def __init__(self):
    self.games_by_id = {}
    self.factions_by_id = {}
    self.units_by_id = {}
    self.models_by_id = {}
    self._data = None

  def load(self):
    self._get_data()
    self._load_games()
    self._load_factions()
    self._load_models()
    self._load_units()
  
  def _get_data(self):
    try:
      with open(filepath, "r") as file:
        data = json.load(file)
        self._data = data
    
    except FileNotFoundError:
      print(f"Error: The file '{filepath}' was not found.")
      sys.exit(1)
    except json.JSONDecodeError:
      print(f"Error: Failed to decode JSON from the file '{filepath}'. The file may be malformed.")
      sys.exit(1)

  def _load_games(self):
    for game in self._data["games"]:
      key = game["game_id"]
      self.games_by_id[key] = Game(game["game_id"], game["game_name"])
  
  def _load_factions(self):
    for faction in self._data["factions"]:
      key = faction["faction_id"]
      self.factions_by_id[key] = Faction(faction["faction_id"], faction["faction_name"], faction["game_id"])
  
  def _load_models(self):
    for model in self._data["models"]:
      key = model["model_id"]
      self.models_by_id[key] = Model(model["model_id"], model["model_name"])
  
  def _load_units(self):
    for unit in self._data["units"]:
      key = unit["unit_id"]
      faction_obj = self.factions_by_id[unit["faction_id"]]
      models = []
      for model in unit["models"]:
        models.append(ModelComposition(self.models_by_id[model["model_id"]], model["min_quantity"], model["max_quantity"]))
      self.units_by_id[key] = Unit(
        unit["unit_id"],
        unit["unit_name"],
        faction_obj,
        unit["base_points"],
        unit["role"],
        unit["keywords"],
        models
      )