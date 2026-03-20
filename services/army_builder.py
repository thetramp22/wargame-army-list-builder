from loaders.game_data import GameData
from models.army import Army
from models.army_unit import ArmyUnit


class ArmyBuilder:
    def __init__(
        self,
        game_data: GameData,
    ):
        self.game_data = game_data

    def create_army(self, name: str, game_id: str, faction_id: str):
        success = True
        messages = []
        if not faction_id in self.game_data.get_factions_by_game(game_id):
            success = False
            messages.append(f"Invalid Faction: {faction_id}")
            return {"success": success, "army": None, "messages": messages}
        faction = self.game_data.get_faction(faction_id)
        army = Army(name, faction)
        return {"success": success, "army": army, "messages": messages}

    def add_unit_to_army(self, unit_id: str, army: Army, quantity: int = 1):
        added_successfully = True
        messages = []
        if quantity == 0:
            added_successfully = False
            messages.append("cannot add 0 units")
        if quantity < 0:
            added_successfully = False
            messages.append("cannot add negative units")
        matching_unit = next(
            (army_unit for army_unit in army.units if army_unit.unit.id == unit_id),
            None,
        )
        if matching_unit:
            matching_unit.quantity += quantity
        else:
            army.units.append(ArmyUnit(self.game_data.get_unit(unit_id), quantity))
        return {"added_successfully": added_successfully, "messages": messages}

    def remove_unit_from_army(self, unit_id: str, army: Army, quantity: int = 1):
        removed_successfully = True
        messages = []
        matching_unit = next(
            (army_unit for army_unit in army.units if army_unit.unit.id == unit_id),
            None,
        )
        if matching_unit is None:
            removed_successfully = False
            messages.append(f"No {unit_id} unit to remove")
        elif matching_unit.quantity > quantity:
            matching_unit.quantity -= quantity
        elif matching_unit.quantity > 0 and matching_unit.quantity < quantity:
            messages.append(
                f"{army.name} only has {matching_unit.quantity} {matching_unit.unit.name} units, all were removed"
            )
            army.units.remove(matching_unit)
        elif matching_unit.quantity == quantity:
            army.units.remove(matching_unit)
        else:
            removed_successfully = False
            messages.append("cannot remove a negative number of units")
        return {"removed_successfully": removed_successfully, "messages": messages}

    def list_army_units(self, army: Army):
        army_units_list = []
        for army_unit in army.units:
            army_units_list.append(
                {"name": army_unit.unit.name, "quantity": army_unit.quantity}
            )
        return army_units_list

    def get_army_summary(self, army: Army):
        return {
            "name": army.name,
            "faction": army.faction.name,
            "points": self.calculate_total_points(army),
        }

    def calculate_total_points(self, army: Army):
        total_points = 0
        for army_unit in army.units:
            total_points += army_unit.unit.base_points * army_unit.quantity
        return total_points

    def validate_army(self, army: Army):
        is_valid_army = True
        error_messages = []

        # all units must be from army's faction
        for army_unit in army.units:
            if army_unit.unit.faction.id != army.faction.id:
                is_valid_army = False
                error_messages.append(
                    f"- {army_unit.unit.name} is not part of the {army.faction.id} faction"
                )

        # point value must be under (or equal to) a points limit
        points_limit = 2000

        if self.calculate_total_points(army) > points_limit:
            is_valid_army = False
            error_messages.append(f"- {army.name} is over {points_limit} points")

        # army can only have a set amount of each unit
        unit_limit = 3

        for army_unit in army.units:
            if army_unit.quantity > unit_limit:
                is_valid_army = False
                error_messages.append(
                    f"- {army.name} has more than {unit_limit} {army_unit.unit.name} units"
                )

        return {"is_valid_army": is_valid_army, "error_messages": error_messages}
