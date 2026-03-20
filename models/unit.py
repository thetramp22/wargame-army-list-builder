from models.faction import Faction
from models.model import Model


class ModelComposition:
    def __init__(self, model: Model, min_quantity: int, max_quantity: int):
        self.model = model
        self.min_quantity = min_quantity
        self.max_quantity = max_quantity


class Unit:
    def __init__(
        self,
        unit_id: str,
        unit_name: str,
        faction: Faction,
        base_points: int,
        role: str,
        keywords: list[str],
        models: list[ModelComposition],
    ):
        self.id = unit_id
        self.name = unit_name
        self.faction = faction
        self.base_points = base_points
        self.role = role
        self.keywords = keywords
        self.models = models

    def __repr__(self):
        return f"""Unit(unit_id='{self.id}',
    unit_name='{self.name}',
    faction_id='{self.faction}',
    base_points='{self.base_points}',
    role='{self.role}',
    keywords='{self.keywords}'.
    models='{self.models}')"""
