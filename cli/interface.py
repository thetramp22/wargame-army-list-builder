import cmd
from loaders.game_data import GameData
from services.army_builder import ArmyBuilder
from services.army_repository import ArmyRepository


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
        """
        arguments = line.split()
        if len(arguments) != 2:
            print("*** invalid number of arguments")
            return
        name, faction_id = arguments
        result = self.army_builder.create_army(name, self.current_game_id, faction_id)
        if not result["success"]:
            for message in result["messages"]:
                print(f"*** {message}")
            return
        self.current_army = result["army"]
        print(f"Army '{name}' created (Faction: {self.current_army.faction.name})")

    def do_add(self, line):
        """Add unit to army"""

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
