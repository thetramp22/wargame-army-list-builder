from models.army_unit import ArmyUnit
from loaders.game_data import GameData

class Army():
  def __init__(self, name, faction_id):
    self.name = name
    self.faction_id = faction_id
    self.units = []

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


  
