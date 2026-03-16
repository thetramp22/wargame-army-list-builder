from loaders.data_loader import DataLoader
from loaders.game_data import GameData
from models.army import Army

def main():
  loader = DataLoader()
  game_data = loader.load()

  army = Army("My Space Marines", "space_marines")
  army.add_unit("intercessor_squad")
  army.add_unit("intercessor_squad")
  army.add_unit("deathwing_knights")
  army.remove_unit("intercessor_squad")

  print(f"Army: {army.name}")
  print(f"Units:")
  for u in army.units:
    print(f"{game_data.units_by_id[u.id].name} x{u.quantity}")

  print(f"Total Points: {calculate_total_points(army, game_data)}")

def calculate_total_points(army: Army, game_data: GameData):
  total_points = 0
  for unit in army.units:
    total_points += game_data.units_by_id[unit.id].base_points
  return total_points

main()