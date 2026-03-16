class GameData():
  def __init__(self):
    self.games_by_id = {}
    self.factions_by_id = {}
    self.units_by_id = {}
    self.models_by_id = {}
    self.models_by_unit = {}
    self.units_by_faction = {}
    self.factions_by_game = {}

  def get_game(self, game_id):
    return self.games_by_id[game_id]

  def get_faction(self, faction_id):
    return self.factions_by_id[faction_id]
  
  def get_unit(self, unit_id):
    return self.units_by_id[unit_id]
  
  def get_model(self, model_id):
    return self.models_by_id[model_id]
  
  def get_models_by_unit(self, unit_id):
    models = []
    for model in self.models_by_unit[unit_id]:
      models.append(self.models_by_id[model])
    return models
  
  def get_units_by_faction(self, faction_id):
    units = []
    for unit in self.units_by_faction[faction_id]:
      units.append(self.units_by_id[unit])
    return units
  
  def get_factions_in_game(self, game_id):
    factions = []
    for faction in self.factions_by_game[game_id]:
      factions.append(self.factions_by_id[faction])
    return factions