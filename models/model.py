class Model():
  def __init__(self, model_id, model_name):
    self.model_id = model_id
    self.model_name = model_name

  def __repr__(self):
    return f"Model(model_id='{self.model_id}', model_name='{self.model_name}')"