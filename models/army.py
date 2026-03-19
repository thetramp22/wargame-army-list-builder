from models.army_unit import ArmyUnit
from loaders.game_data import GameData
from models.faction import Faction

class Army():
  def __init__(self, name: str, faction: Faction, units: list[ArmyUnit] = []):
    self.name = name
    self.faction = faction
    self.units = units

  def to_dict(self):
    army_unit_dict = [unit.to_dict() for unit in self.units]
    faction_dict = {"id": self.faction.id, "name": self.faction.name, "game_id": self.faction.game_id}
    return {"name": self.name, "faction": faction_dict, "units": army_unit_dict}