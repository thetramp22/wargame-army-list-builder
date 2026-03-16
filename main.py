from loaders.data_loader import DataLoader
from models.army import Army

def main():
  loader = DataLoader()
  game_data = loader.load()

  army = Army("My Space Marines", "space_marines")
  army.add_unit("intercessor_squad")
  army.add_unit("intercessor_squad")
  army.add_unit("deathwing_knights")
  army.remove_unit("intercessor_squad")
  army.remove_unit("intercessor_squad")
  army.remove_unit("intercessor_squad")

  print(f"Army: {army.name}")
  print(f"Units:")
  for u in army.units:
    print(f"{game_data.units_by_id[u.id].name} x{u.quantity}")

main()