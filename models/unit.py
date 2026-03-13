class Unit():
  def __init__(self, unit_id, unit_name, faction_id, base_points, role, keywords, models):
    self.unit_id = unit_id
    self.unit_name = unit_name
    self.faction_id = faction_id
    self.base_points = base_points
    self.role = role
    self.keywords = keywords
    self.models = models

  def __repr__(self):
    return f"""Unit(unit_id='{self.unit_id}',
    unit_name='{self.unit_name}',
    faction_id='{self.faction_id}',
    base_points='{self.base_points}',
    role='{self.role}',
    keywords='{self.keywords}'.
    models='{self.models}')"""