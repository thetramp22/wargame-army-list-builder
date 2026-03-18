from loaders.data_loader import DataLoader
from services.army_builder import ArmyBuilder
from cli.interface import Interface

filepath = "./data/armies.json"

interface = Interface()

def main():
  loader = DataLoader()
  game_data = loader.load()
  army_builder = ArmyBuilder(game_data, filepath)
  
  army = army_builder.load_army_from_file("big blue")

  army_builder.list_army_units(army)
  army_builder.show_army_summary(army)
  army_builder.validate_army(army)

# if __name__ == '__main__':
#     interface.cmdloop()

main()