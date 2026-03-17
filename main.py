from loaders.data_loader import DataLoader
from loaders.game_data import GameData
from models.army import Army
from models.faction import Faction
from services.army_builder import ArmyBuilder
from cli.interface import Interface
import os
import json
import sys

interface = Interface()

def main():
  loader = DataLoader()
  game_data = loader.load()
  army_builder = ArmyBuilder(game_data)
  
  army = army_builder.load_army_from_file("big blue")

  army_builder.list_army_units(army)
  army_builder.show_army_summary(army)
  army_builder.validate_army(army)

# if __name__ == '__main__':
#     interface.cmdloop()

main()