class Model:
    def __init__(self, model_id: str, model_name: str):
        self.id = model_id
        self.name = model_name

    def __repr__(self):
        return f"Model(model_id='{self.id}', model_name='{self.name}')"
