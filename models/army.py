from models.army_unit import ArmyUnit
from loaders.game_data import GameData

class Army():
  def __init__(self, name: str, faction_id: str):
    self.name = name
    self.faction_id = faction_id
    self.units: list[ArmyUnit] = []

  def add_unit(self, unit_id):
    matching_unit = next((unit for unit in self.units if unit.id == unit_id), None)

    if matching_unit:
      matching_unit.quantity += 1
    else:
      self.units.append(ArmyUnit(unit_id, 1))

  def remove_unit(self, unit_id):
    matching_unit = next((unit for unit in self.units if unit.id == unit_id), None)

    if matching_unit == None:
      return
    elif matching_unit.quantity > 1:
      matching_unit.quantity -= 1
    else:
      self.units.remove(matching_unit)

  def to_dict(self):
    army_unit_dict = [unit.to_dict() for unit in self.units]
    return {"name": self.name, "faction_id": self.faction_id, "units": army_unit_dict}


  
