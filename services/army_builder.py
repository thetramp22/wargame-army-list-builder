from loaders.game_data import GameData
from models.army import Army
from models.army_unit import ArmyUnit
import os
import json

class ArmyBuilder():
  def __init__(self, game_data: GameData, filepath: str) -> None:
    self.game_data = game_data
    self.filepath = filepath

  def create_army(self, name, faction_id):
    faction = self.game_data.get_faction(faction_id)
    return Army(name, faction)

  def add_unit_to_army(self, unit_id: str, army: Army | None):
    if army == None:
      raise Exception("army should not be None")
    matching_unit = next((army_unit for army_unit in army.units if army_unit.unit.id == unit_id), None)
    if matching_unit:
      matching_unit.quantity += 1
    else:
      army.units.append(ArmyUnit(self.game_data.get_unit(unit_id), 1))

  def remove_unit_from_army(self, unit_id: str, army: Army | None):
    if army == None:
      raise Exception("army should not be None")
    matching_unit = next((army_unit for army_unit in army.units if army_unit.unit.id == unit_id), None)

    if matching_unit == None:
      raise Exception(f"No {unit_id} unit to remove")
    elif matching_unit.quantity > 1:
      matching_unit.quantity -= 1
    else:
      army.units.remove(matching_unit)

  def list_army_units(self, army: Army | None):
    if army == None:
      raise Exception("army should not be None")
    army_units_list = []
    for army_unit in army.units:
      army_units_list.append({"name":army_unit.unit.name, "quantity": army_unit.quantity})
    return army_units_list

  def get_army_summary(self, army: Army | None):
    if army is None:
      raise Exception("army should not be None")
    return {"name": army.name,
            "faction": army.faction.name,
            "points": self.calculate_total_points(army)}

  def calculate_total_points(self, army: Army | None):
    if army == None:
      raise Exception("army should not be None")
    total_points = 0
    for army_unit in army.units:
      total_points += army_unit.unit.base_points * army_unit.quantity
    return total_points

  def validate_army(self, army: Army | None):
    if army == None:
      raise Exception("army should not be None")
    is_valid_army = True
    error_messages = []

    # all units must be from army's faction
    for army_unit in army.units:
      if army_unit.unit.faction.id != army.faction.id:
        is_valid_army = False
        error_messages.append(f"- {army_unit.unit.name} is not part of the {army.faction.id} faction")

    # point value must be under (or equal to) a points limit
    points_limit = 2000

    if self.calculate_total_points(army) > points_limit:
      is_valid_army = False
      error_messages.append(f"- {army.name} is over {points_limit} points")

    # army can only have a set amount of each unit
    unit_limit = 3

    for army_unit in army.units:
      if army_unit.quantity > unit_limit:
        is_valid_army = False
        error_messages.append(f"- {army.name} has more than {unit_limit} {army_unit.unit.name} units")

    return {"is_valid_army": is_valid_army, "error_messages": error_messages}
  

  # to be moved to separate module later on
  def save_army_to_file(self, army: Army | None):
    if army == None:
      raise Exception("army should not be None")
    
    army_data = army.to_dict()
    saved_successfully = True
    messages = []
    if not os.path.exists(self.filepath):
      messages.append(f"Armies file not found, creating new file at: {self.filepath}")
      with open(self.filepath, 'w') as file:
        json.dump({"armies": {}}, file, indent=2)
    try:
      with open(self.filepath, 'r') as file:
        file_data = json.load(file)
    except FileNotFoundError:
      messages.append(f"Error: The file '{self.filepath}' was not found.")
      saved_successfully = False
      return {"saved_successfully": saved_successfully, "messages": messages}
    except json.JSONDecodeError:
      messages.append(f"Error: Failed to decode JSON from the file '{self.filepath}'. The file may be malformed.")
      saved_successfully = False
      return {"saved_successfully": saved_successfully, "messages": messages}

    file_data["armies"][army.name] = army_data

    with open(self.filepath, 'w') as file:
      json.dump(file_data, file, indent=2)

    return {"saved_successfully": saved_successfully, "messages": messages}

  def load_army_from_file(self, army_name: str):
    loaded_successfully = True
    messages = []
    try:
      with open(self.filepath, 'r') as file:
        file_data = json.load(file)
    except FileNotFoundError:
      print(f"Error: The file '{self.filepath}' was not found.")
      loaded_successfully = False
      return {"loaded_successfully": loaded_successfully, "messages": messages}
    except json.JSONDecodeError:
      print(f"Error: Failed to decode JSON from the file '{self.filepath}'. The file may be malformed.")
      loaded_successfully = False
      return {"loaded_successfully": loaded_successfully, "messages": messages}

    army_to_load = None
    if army_name in file_data["armies"]:
      army_data = file_data["armies"][army_name]
      faction = self.game_data.factions_by_id[army_data["faction"]["id"]]
      army_to_load = Army(army_data["name"], faction)
      for unit in army_data["units"]:
        for _ in range(0, unit["quantity"]):
          self.add_unit_to_army(unit["id"], army_to_load)
    else:
      loaded_successfully = False
      messages.append(f"No army named {army_name} found in {self.filepath}")
    return {"loaded_successfully": loaded_successfully, "messages": messages}