from loaders.data_loader import DataLoader

def main():
  loader = DataLoader()
  game_data = loader.load()

  print(f"games loaded: {len(game_data.games_by_id)}")
  print(f"factions loaded: {len(game_data.factions_by_id)}")
  print(f"models loaded: {len(game_data.models_by_id)}")
  print(f"units loaded: {len(game_data.units_by_id)}")

  units = game_data.units_by_faction["space_marines"]
  for u in units:
    print(u)

  factions = game_data.factions_by_game["warhammer_40k"]
  for f in factions:
    print(f)

main()