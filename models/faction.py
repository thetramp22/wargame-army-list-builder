class Faction():
  def __init__(self, faction_id: str, faction_name: str, game_id: str):
    self.id = faction_id
    self.name = faction_name
    self.game_id = game_id


  def __repr__(self):
    return f"Faction(faction_id='{self.id}', faction_name='{self.name}', game_id='{self.game_id}')"