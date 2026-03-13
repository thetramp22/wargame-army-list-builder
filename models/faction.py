class Faction():
  def __init__(self, faction_id, faction_name):
    self.faction_id = faction_id
    self.faction_name = faction_name

  def __repr__(self):
    return f"Faction(faction_id='{self.faction_id}', faction_name='{self.faction_name}')"