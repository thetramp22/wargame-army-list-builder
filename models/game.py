class Game():
  def __init__(self, game_id, game_name):
    self.game_id = game_id
    self.game_name = game_name

  def __repr__(self):
    return f"Game(game_id='{self.game_id}', game_name='{self.game_name}')"