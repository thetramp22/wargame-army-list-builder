import cmd
from loaders.game_data import GameData
from services.army_builder import ArmyBuilder
from services.army_repository import ArmyRepository
import shlex


class Interface(cmd.Cmd):
    prompt = "ArmyBldr>> "
    intro = "ArmyBuilderCLI, Type 'help' for available commands."

    def __init__(
        self,
        game_data: GameData,
        army_builder: ArmyBuilder,
        army_repository: ArmyRepository,
    ):
        super().__init__()
        self.game_data = game_data
        self.army_builder = army_builder
        self.army_repository = army_repository
        self.current_army = None
        # for future support of multiple games, currently only 1 game supported
        self.current_game_id = "warhammer_40k"

    def do_create(self, line):
        """Create a new army

        Usage: create <name> <faction_id>
        Creates a new army with the given name and faction.
        Example: create my_army space_marines
        Army names may include spaces if enclosed in quotes.
        Example: create "My Army" space_marines
        """
        arguments = shlex.split(line)
        if len(arguments) != 2:
            print("*** invalid number of arguments")
            return
        name, faction_id = arguments
        if self.current_army is not None:
            confirm = input(
                f"""Army '{self.current_army.name}' is currently loaded.
                            Creating a new army will overwrite the current army and any unsaved progress will be lost.
                            Do you wish to proceed? (y/n): """
            )
            if confirm.lower() != "y":
                print("Army creation cancelled")
                return
        result = self.army_builder.create_army(name, self.current_game_id, faction_id)
        if not result["success"]:
            for message in result["messages"]:
                print(f"*** {message}")
            return
        self.current_army = result["army"]
        print(f"Army '{name}' created (Faction: {self.current_army.faction.name})")

    def do_add(self, line):
        """Add unit to army

        Usage: add <unit_id> <quantity>
        Adds the give quantity of a unit to the current army.
        Example: add intercessor_squad 2
        """
        if self.current_army is None:
            print("*** No army to add to, please create or load an army")
            return
        arguments = shlex.split(line)
        if len(arguments) == 0 or len(arguments) > 2:
            print("*** invalid number of arguments")
            return
        unit_id = arguments[0]
        if len(arguments) == 1:
            quantity = 1
        if len(arguments) == 2:
            try:
                quantity = int(arguments[1])
            except ValueError:
                print("*** <quantity> must be an integer")
                return
        result = self.army_builder.add_unit_to_army(
            unit_id, self.current_army, quantity
        )
        if not result["success"]:
            for message in result["messages"]:
                print(f"*** {message}")
            return
        army_unit = result["unit"]
        print(
            f"Added {quantity} {army_unit.unit.name} units to {self.current_army.name}"
        )

    def do_remove(self, line):
        """Remove unit from army

        Usage: remove <unit_id> <quantity>
        Removes the give quantity of a unit from the current army.
        Example: remove intercessor_squad 2
        """
        if self.current_army is None:
            print("*** No army loaded, please create or load an army")
            return
        arguments = shlex.split(line)
        if len(arguments) == 0 or len(arguments) > 2:
            print("*** invalid number of arguments")
            return
        unit_id = arguments[0]
        if len(arguments) == 1:
            quantity = 1
        if len(arguments) == 2:
            try:
                quantity = int(arguments[1])
            except ValueError:
                print("*** <quantity> must be an integer")
                return
        result = self.army_builder.remove_unit_from_army(
            unit_id, self.current_army, quantity
        )
        if not result["success"]:
            for message in result["messages"]:
                print(f"*** {message}")
            return
        army_unit = result["unit"]
        print(
            f"Removed {quantity} {army_unit.unit.name} units from {self.current_army.name}"
        )

    def do_show(self, line):
        """Show summary of current army

        Usage: show
        Shows the name, faction, unit list, and total points of the current army.
        """
        if self.current_army is None:
            print("*** No army to show, please create or load an army")
            return
        if line:
            print("*** invalid number of arguments")
            return
        print(f"    Army: {self.current_army.name}")
        print(f"    Faction: {self.current_army.faction.name}")
        for unit in self.current_army.units:
            print(f"    - {unit.unit.name} x{unit.quantity}")
        print(
            f"    Total Points: {self.army_builder.calculate_total_points(self.current_army)}"
        )

    def do_save(self, line):
        """Save current army to file

        Usage: save
        Saves the current army to file.
        """
        if self.current_army is None:
            print("*** No army to save, please create or load an army")
            return
        result = self.army_repository.save(self.current_army)
        if not result["success"]:
            for message in result["messages"]:
                print(f"*** {message}")
                return
        print(f"Army '{self.current_army.name}' saved")

    def do_load(self, line):
        """Load army from file

        Usage: load <army_name>
        Loads the given army from file.
        Example: load my_army
        Example: load "My Army"
        """
        arguments = shlex.split(line)
        if len(arguments) != 1:
            print("*** invalid number of arguments")
            return
        army = arguments[0]
        result = self.army_repository.load(army, self.game_data)
        if not result["success"]:
            for message in result["messages"]:
                print(f"*** {message}")
                return
        if self.current_army is not None:
            confirm = input(
                f"""Army '{self.current_army.name}' is currently loaded.
                            Creating a new army will overwrite the current army and any unsaved progress will be lost.
                            Do you wish to proceed? (y/n): """
            )
            if confirm.lower() != "y":
                print("Army load cancelled")
                return
        self.current_army = result["army"]
        print(f"Army '{army}' loaded")

    def do_list(self, line):
        """List armies from file

        Usage: list
        Lists all armies saved to file.
        """
        if line:
            print("*** invalid number of arguments")
            return
        result = self.army_repository.list()
        if not result["success"]:
            for message in result["messages"]:
                print(f"*** {message}")
                return
        print("    Armies in file:")
        for army in result["lst"]:
            print(f"    - {army}")

    def do_delete(self, line):
        """Delete army from file

        Usage: delete <army_name>
        Deletes given army from file.
        Example: delete my_army
        Example: delete "My Army"
        """
        arguments = shlex.split(line)
        if len(arguments) != 1:
            print("*** invalid number of arguments")
            return
        army = arguments[0]
        confirm = input(
            f"""This will permanently delete '{army}'.
                Do you wish to proceed? (y/n): """
        )
        if confirm.lower() != "y":
            print("Army load cancelled")
            return
        result = self.army_repository.delete(army)
        if not result["success"]:
            for message in result["messages"]:
                print(f"*** {message}")
                return
        print(f"'{army}' army deleted")

    def do_validate(self, line):
        """Check that current army is valid

        Usage: validate
        Checks that current army is valid for play.
        """
        if self.current_army is None:
            print("*** No army to show, please create or load an army")
            return
        if line:
            print("*** invalid number of arguments")
            return
        result = self.army_builder.validate_army(self.current_army)
        if not result["success"]:
            for message in result["messages"]:
                print(f"*** {message}")
            print(f"Army '{self.current_army.name}' is not a valid")
            return

    def do_quit(self, line):
        """Exit the CLI"""
        return True

    def postcmd(self, stop, line):
        print()  # Add an empty line for better readability
        return stop
