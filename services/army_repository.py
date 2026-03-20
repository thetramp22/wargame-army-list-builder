from models.army import Army
from models.army_unit import ArmyUnit
from loaders.game_data import GameData
from typing import TypedDict
import json
import os


class ReturnArmyStatus(TypedDict):
    success: bool
    army: Army | None
    messages: list[str]


class FileReadStatus(TypedDict):
    success: bool
    data: dict
    messages: list[str]


class FileWriteStatus(TypedDict):
    success: bool
    messages: list[str]


class ListStatus(TypedDict):
    success: bool
    lst: list[str]
    messages: list[str]


class DeleteStatus(TypedDict):
    success: bool
    messages: list[str]


class ArmyRepository:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def _read_file(self) -> FileReadStatus:
        success = True
        data = {"armies": {}}
        messages = []
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            messages.append(f"No armies file found, returning default army data.")
        except json.JSONDecodeError:
            messages.append(
                f"Failed to decode JSON from the file {self.filepath}. The file may be malformed"
            )
            success = False
        if not isinstance(data, dict):
            success = False
            messages.append("Invalid file structure.")
        if not "armies" in data:
            success = False
            messages.append("Invalid file structure.")
        if not isinstance(data["armies"], dict):
            success = False
            messages.append("Invalid file structure.")
        return {"success": success, "data": data, "messages": messages}

    def _write_file(self, data) -> FileWriteStatus:
        success = True
        messages = []
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        try:
            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=2)
        except PermissionError:
            messages.append(
                f"Permission denied when trying to write to '{self.filepath}'."
            )
            success = False
        return {"success": success, "messages": messages}

    def _build_army_from_dict(self, army_data: dict, game_data: GameData) -> Army:
        faction = game_data.factions_by_id[army_data["faction"]["id"]]
        units = []
        for unit in army_data["units"]:
            units.append(ArmyUnit(game_data.units_by_id[unit["id"]], unit["quantity"]))
        return Army(army_data["name"], faction, units)

    def _validate_army_data(self, army_data: dict, game_data: GameData) -> dict:
        is_valid = True
        messages = []
        try:
            faction_id = army_data["faction"]["id"]
            if faction_id not in game_data.factions_by_id:
                messages.append(f"Invalid faction: {faction_id}")
                is_valid = False
            for unit in army_data["units"]:
                unit_id = unit["id"]
                if unit_id not in game_data.units_by_id:
                    messages.append(f"Invalid unit: {unit_id}")
                    is_valid = False
                unit_quantity = unit["quantity"]
                if not isinstance(unit_quantity, int):
                    messages.append(
                        f"Invalid unit quantity: {unit_quantity}, must be an integer"
                    )
                    is_valid = False
                if not unit_quantity > 0:
                    messages.append(
                        f"Invalid unit quantity: {unit_quantity}, must be greater than 0"
                    )
                    is_valid = False
        except KeyError as e:
            is_valid = False
            messages.append(f"Key not found: {e}")
        return {"success": is_valid, "messages": messages}

    def save(self, army: Army) -> ReturnArmyStatus:
        success = True
        messages = []
        read_status = self._read_file()
        messages += read_status["messages"]
        if not read_status["success"]:
            return {
                "success": read_status["success"],
                "army": army,
                "messages": messages,
            }
        armies_data = read_status["data"]["armies"]
        army_data = army.to_dict()
        armies_data[army_data["name"]] = army_data
        write_status = self._write_file(armies_data)
        if not write_status["success"]:
            success = False
            messages += write_status["messages"]
        return {"success": success, "army": army, "messages": messages}

    def load(self, name: str, game_data: GameData) -> ReturnArmyStatus:
        success = True
        army = None
        messages = []
        file_status = self._read_file()
        messages += file_status["messages"]
        if not file_status["success"]:
            return {
                "success": file_status["success"],
                "army": army,
                "messages": messages,
            }
        if not name in file_status["data"]["armies"]:
            messages.append(f"Army not found: {name}")
            return {"success": False, "army": army, "messages": messages}
        army_data = file_status["data"]["armies"][name]
        validation = self._validate_army_data(army_data, game_data)
        messages += validation["messages"]
        if not validation["success"]:
            return {"success": False, "army": army, "messages": messages}
        army = self._build_army_from_dict(army_data, game_data)
        return {"success": success, "army": army, "messages": messages}

    def list(self) -> ListStatus:
        success = True
        lst = []
        messages = []
        file_status = self._read_file()
        messages += file_status["messages"]
        if not file_status["success"]:
            return {"success": file_status["success"], "lst": lst, "messages": messages}
        lst = file_status["data"]["armies"].keys()
        return {"success": success, "lst": lst, "messages": messages}

    def delete(self, name: str) -> DeleteStatus:
        success = True
        messages = []
        file_status = self._read_file()
        messages += file_status["messages"]
        if not file_status["success"]:
            return {"success": file_status["success"], "messages": messages}
        file_data = file_status["data"]
        if name not in file_data["armies"]:
            success = False
            messages.append(f"No army named {name} to delete")
            return {"success": success, "messages": messages}
        del file_data["armies"][name]
        write_status = self._write_file(file_data)
        if not write_status["success"]:
            success = False
            messages += write_status["messages"]
        return {"success": success, "messages": messages}
