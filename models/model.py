class Model():
  def __init__(self, model_id, model_name):
    self.id = model_id
    self.name = model_name

  def __repr__(self):
    return f"Model(model_id='{self.id}', model_name='{self.name}')"