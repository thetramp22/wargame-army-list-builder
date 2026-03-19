from loaders.data_loader import DataLoader
from services.army_builder import ArmyBuilder
from cli.interface import Interface

filepath = "./data/armies.json"

interface = Interface()

def main():
  loader = DataLoader()
  game_data = loader.load()
  army_builder = ArmyBuilder(game_data, filepath)
  

# if __name__ == '__main__':
#     interface.cmdloop()

main()