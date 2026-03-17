from models.unit import Unit

class ArmyUnit():
  def __init__(self, unit: Unit, quantity: int):
    self.unit = unit
    self.quantity = quantity

  def to_dict(self):
    return {"id": self.unit.id, "quantity": self.quantity}