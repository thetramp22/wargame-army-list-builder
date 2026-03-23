from loaders.data_loader import DataLoader
from services.army_builder import ArmyBuilder
from services.army_repository import ArmyRepository
from cli.interface import Interface

filepath = "./data/armies.json"


def main():
    loader = DataLoader()
    game_data = loader.load()
    army_builder = ArmyBuilder(game_data)
    army_repository = ArmyRepository(filepath)
    interface = Interface(game_data, army_builder, army_repository)
    interface.cmdloop()


if __name__ == "__main__":
    main()
