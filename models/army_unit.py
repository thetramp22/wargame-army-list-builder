class ArmyUnit():
  def __init__(self, unit_id: str, quantity: int):
    self.id = unit_id
    self.quantity = quantity

  def to_dict(self):
    return {"id": self.id, "quantity": self.quantity}