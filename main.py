from loaders.data_loader import DataLoader

def main():
  loader = DataLoader()
  loader.load()

  print(f"games loaded: {len(loader.games_by_id)}")
  print(f"factions loaded: {len(loader.factions_by_id)}")
  print(f"models loaded: {len(loader.models_by_id)}")
  print(f"units loaded: {len(loader.units_by_id)}")

  factions = loader.get_factions_in_game("warhammer_40k")
  for f in factions:
    print(f.faction_id)

main()