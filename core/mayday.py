class Mayday:

    def __init__(self):
        print("Initializing MAYDAY...")

    def start(self):
        print("MAYDAY Started")
        
        while True:
            command = input("you : ")
            
            if command.lower() == "exit":
                print("Exiting MAYDAY...")
                break
            
            print(f"MAYDAY : you said '{command}'")
            