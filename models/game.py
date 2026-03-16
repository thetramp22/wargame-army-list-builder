class Game():
  def __init__(self, game_id, game_name):
    self.id = game_id
    self.name = game_name

  def __repr__(self):
    return f"Game(game_id='{self.id}', game_name='{self.name}')"