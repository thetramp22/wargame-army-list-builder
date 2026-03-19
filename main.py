from loaders.data_loader import DataLoader
from services.army_builder import ArmyBuilder
from cli.interface import Interface

interface = Interface()

def main():
  loader = DataLoader()
  game_data = loader.load()
  

# if __name__ == '__main__':
#     interface.cmdloop()

main()