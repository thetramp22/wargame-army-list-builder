class GameData():
  def __init__(self):
    self.games_by_id = {}
    self.factions_by_id = {}
    self.units_by_id = {}
    self.models_by_id = {}
    self.units_by_faction = {}
    self.factions_by_game = {}

  def get_factions_in_game(self, game_id):
    factions = []
    for faction in self.factions_by_id.values():
      if faction.game_id == game_id:
        factions.append(faction)
    return factions

  def get_faction(self, faction_id):
    return self.factions_by_id[faction_id]