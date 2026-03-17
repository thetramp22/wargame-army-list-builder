import cmd

class Interface(cmd.Cmd):
  prompt = "ArmyBldr>> "
  intro = "ArmyBuilderCLI, Type 'help' for available commands."

  def __init__(self):
    super().__init__()

  def do_create_army(self, line):
    """Create a new army"""
    pass

  def do_test(self, line):
    """Test command"""
    print("Test command output")

  def do_quit(self, line):
    """Exit the CLI"""
    return True
  
  def postcmd(self, stop, line):
    print()  # Add an empty line for better readability
    return stop