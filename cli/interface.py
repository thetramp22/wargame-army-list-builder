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
        arguments = shlex.split(line)
        if len(arguments) != 2:
            print("*** invalid number of arguments")
            return
        unit_id = arguments[0]
        try:
            quantity = int(arguments[1])
        except ValueError:
            print("*** <quantity> must be an integer")
            return
        if self.current_army is None:
            print("*** No army to add to, please create or load an army")
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
            f"Added {army_unit.quantity} {army_unit.unit.name} units to {self.current_army.name}"
        )

    def do_show(self, line):
        """Show summary of current army"""

    def do_save(self, line):
        """Save current army to file"""

    def do_load(self, line):
        """Load army from file"""

    def do_list(self, line):
        """List armies from file"""

    def do_delete(self, line):
        """Delete army from file"""

    def do_validate(self, line):
        """Check that current army is valid for play"""

    def do_test(self, line):
        """Test command"""
        print("Test command output")

    def do_quit(self, line):
        """Exit the CLI"""
        return True

    def postcmd(self, stop, line):
        print()  # Add an empty line for better readability
        return stop
