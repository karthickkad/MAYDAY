from core.banner import Banner
from core.commands import CommandManager
from core.logger import Logger
from core.config import Config
class Mayday:

    def __init__(self):
        Logger.info("Initializing MAYDAY...")
        
        self.config = Config()
        self.command_manager = CommandManager()

    def start(self):
        if self.config.get("console", "show_banner"):
            Banner.show()

        while True:
            command = self.get_command()

            if command.lower() == "exit":
                self.shutdown()
                break

            self.process_command(command)

    def get_command(self):
        prompt = self.config.get("console", "prompt")
        return input(prompt)

    def process_command(self, command):
        Logger.info(f"Processing command: {command}")
        self.command_manager.execute(command)

    def shutdown(self):
        Logger.info("\nShutting down MAYDAY...")
        print("Goodbye!\n")