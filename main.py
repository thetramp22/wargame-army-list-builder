from loaders.data_loader import DataLoader
from loaders.game_data import GameData
from models.army import Army
from cli.interface import Interface
import json
import sys

army_data_filename = "./data/armies.json"
interface = Interface()

def main():
  loader = DataLoader()
  game_data = loader.load()

def save_army_to_file(army: Army, filename: str):
  army_data = army.to_dict()

  try:
    with open(filename, 'r') as file:
      file_data = json.load(file)
  except FileNotFoundError:
    print(f"Error: The file '{filename}' was not found.")
    sys.exit(1)
  except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from the file '{filename}'. The file may be malformed.")
    sys.exit(1)

  file_data["armies"][army.name] = army_data

  with open(filename, 'w') as file:
    json.dump(file_data, file, indent=2)
    print(f"{army.name} saved successfully to {filename}")

def load_army_from_file(army_name: str, filename: str):
  try:
    with open(filename, 'r') as file:
      file_data = json.load(file)
  except FileNotFoundError:
    print(f"Error: The file '{filename}' was not found.")
    sys.exit(1)
  except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from the file '{filename}'. The file may be malformed.")
    sys.exit(1)

  if file_data["armies"][army_name]:
    army_data = file_data["armies"][army_name]
    army_to_load = Army(army_data["name"], army_data["faction_id"])
    for unit in army_data["units"]:
      for _ in range(0, unit["quantity"]):
        army_to_load.add_unit(unit["id"])
  return army_to_load

def calculate_total_points(army: Army, game_data: GameData):
  total_points = 0
  for unit in army.units:
    total_points += game_data.units_by_id[unit.id].base_points * unit.quantity
  return total_points

def validate_army(army: Army, game_data: GameData):
  is_valid_army = True

  # all units must be from army's faction
  for unit in army.units:
    if game_data.units_by_id[unit.id].faction.id != army.faction_id:
      is_valid_army = False
      print(f"{game_data.units_by_id[unit.id].name} is not part of the {army.faction_id} faction")

  # point value must be under (or equal to) a points limit
  points_limit = 2000

  if calculate_total_points(army, game_data) > points_limit:
    is_valid_army = False
    print(f"{army.name} is over {points_limit} points")

  # army can only have a set amount of each unit
  unit_limit = 3

  for unit in army.units:
    if unit.quantity > unit_limit:
      is_valid_army = False
      print(f"{army.name} has more than {unit_limit} {game_data.units_by_id[unit.id].name} units")

  if is_valid_army:
    print(f"{army.name} is a valid army")
  else:
    print(f"{army.name} is not a valid army")

  return is_valid_army

if __name__ == '__main__':
    interface.cmdloop()