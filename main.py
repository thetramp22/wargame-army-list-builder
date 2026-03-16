from loaders.data_loader import DataLoader
from loaders.game_data import GameData
from models.army import Army

def main():
  loader = DataLoader()
  game_data = loader.load()

  army = Army("My Space Marines", "space_marines")
  army.add_unit("intercessor_squad")
  army.add_unit("boyz")
  army.add_unit("deathwing_knights")
  army.add_unit("deathwing_knights")
  army.add_unit("deathwing_knights")
  army.add_unit("hellblaster_squad")
  army.add_unit("hellblaster_squad")
  army.add_unit("hellblaster_squad")
  army.add_unit("azrael")
  army.add_unit("azrael")
  army.add_unit("azrael")
  army.add_unit("inner_circle_companions")
  army.add_unit("inner_circle_companions")
  army.add_unit("inner_circle_companions")
  army.add_unit("librarian")

  print(f"Army: {army.name}")
  print(f"Units:")
  for u in army.units:
    print(f"{game_data.units_by_id[u.id].name} x{u.quantity}")

  print(f"Total Points: {calculate_total_points(army, game_data)}")

  validate_army(army, game_data)

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

main()