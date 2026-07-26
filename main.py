from core.mayday import Mayday
from core.logger import Logger

def main():
    Logger.setup()
    
    mayday = Mayday()
    mayday.start()


if __name__ == "__main__":
    main()