class ModelComposition():
  def __init__(self, model, min_quantity, max_quantity):
    self.model = model
    self.min_quantity = min_quantity
    self.max_quantity = max_quantity

class Unit():
  def __init__(self, unit_id, unit_name, faction_id, base_points, role, keywords, models):
    self.id = unit_id
    self.name = unit_name
    self.faction_id = faction_id
    self.base_points = base_points
    self.role = role
    self.keywords = keywords
    self.models = models

  def __repr__(self):
    return f"""Unit(unit_id='{self.id}',
    unit_name='{self.name}',
    faction_id='{self.faction_id}',
    base_points='{self.base_points}',
    role='{self.role}',
    keywords='{self.keywords}'.
    models='{self.models}')"""