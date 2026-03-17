from loaders.game_data import GameData
from loaders.data_loader import DataLoader
from models.army import Army
from models.army_unit import ArmyUnit
from models.faction import Faction
import os
import sys
import json

filepath = "./data/armies.json"

class ArmyBuilder():
  def __init__(self, game_data: GameData) -> None:
    self.game_data = game_data

  def create_army(self, name, faction_id):
    faction = self.game_data.get_faction(faction_id)
    return Army(name, faction)

  def add_unit_to_army(self, unit_id: str, army: Army):
    matching_unit = next((army_unit for army_unit in army.units if army_unit.unit.id == unit_id), None)
    if matching_unit:
      matching_unit.quantity += 1
    else:
      army.units.append(ArmyUnit(self.game_data.get_unit(unit_id), 1))

  def remove_unit_from_army(self, unit_id: str, army: Army):
    matching_unit = next((army_unit for army_unit in army.units if army_unit.unit.id == unit_id), None)

    if matching_unit == None:
      return
    elif matching_unit.quantity > 1:
      matching_unit.quantity -= 1
    else:
      army.units.remove(matching_unit)

  def list_army_units(self, army: Army):
    print("Units: ")
    for army_unit in army.units:
      print(f"- {army_unit.unit.name} x{army_unit.quantity}")

  def show_army_summary(self, army: Army):
    print(f"Army summary for {army.name}:")
    print(f"  Faction: {army.faction.name}")
    print(f"  Total points: {self.calculate_total_points(army)}")

  def save_army_to_file(self, army: Army):
    army_data = army.to_dict()

    if not os.path.exists(filepath):
      print(f"Armies file not found, creating new file at: {filepath}")
      with open(filepath, 'w') as file:
        json.dump({"armies": {}}, file, indent=2)
    try:
      with open(filepath, 'r') as file:
        file_data = json.load(file)
    except FileNotFoundError:
      print(f"Error: The file '{filepath}' was not found.")
      sys.exit(1)
    except json.JSONDecodeError:
      print(f"Error: Failed to decode JSON from the file '{filepath}'. The file may be malformed.")
      sys.exit(1)

    file_data["armies"][army.name] = army_data

    with open(filepath, 'w') as file:
      json.dump(file_data, file, indent=2)
      print(f"{army.name} saved successfully to {filepath}")

  def load_army_from_file(self, army_name: str):
    try:
      with open(filepath, 'r') as file:
        file_data = json.load(file)
    except FileNotFoundError:
      print(f"Error: The file '{filepath}' was not found.")
      sys.exit(1)
    except json.JSONDecodeError:
      print(f"Error: Failed to decode JSON from the file '{filepath}'. The file may be malformed.")
      sys.exit(1)

    if file_data["armies"][army_name]:
      army_data = file_data["armies"][army_name]
      faction = Faction(
        army_data["faction"]["id"],
        army_data["faction"]["name"],
        army_data["faction"]["game_id"])
      army_to_load = Army(army_data["name"], faction)
      for unit in army_data["units"]:
        for _ in range(0, unit["quantity"]):
          self.add_unit_to_army(unit["id"], army_to_load)
      print(f"{army_to_load.name} loaded from {filepath}")
    else:
      print(f"No army named {army_name} found in {filepath}")
    return army_to_load
      

  def calculate_total_points(self, army: Army):
    total_points = 0
    for army_unit in army.units:
      total_points += army_unit.unit.base_points * army_unit.quantity
    return total_points

  def validate_army(self, army: Army):
    print(f"Validating army: '{army.name}'")
    is_valid_army = True

    # all units must be from army's faction
    for army_unit in army.units:
      if self.game_data.units_by_id[army_unit.unit.id].faction.id != army.faction.id:
        is_valid_army = False
        print(f"- {army_unit.unit.name} is not part of the {army.faction.id} faction")

    # point value must be under (or equal to) a points limit
    points_limit = 2000

    if self.calculate_total_points(army) > points_limit:
      is_valid_army = False
      print(f"- {army.name} is over {points_limit} points")

    # army can only have a set amount of each unit
    unit_limit = 3

    for army_unit in army.units:
      if army_unit.quantity > unit_limit:
        is_valid_army = False
        print(f"- {army.name} has more than {unit_limit} {army_unit.unit.name} units")

    if is_valid_army:
      print(f"**{army.name} is a valid army**")
    else:
      print(f"**{army.name} is not a valid army**")

    return is_valid_army