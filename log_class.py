import datetime
import json

class GameLog:
    def __init__(self):
        self.logs = []
        
    def add_log(self, player_name, card_used, turn_number):
        log_entry = {
            "player_name": player_name,
            "card_used": card_used,
            "turn_number": turn_number,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.logs.append(log_entry)
    
    def save_to_file(self, filename="game_logs.json"):
        with open(filename, "w") as file:
            json.dump(self.logs, file, indent=4)

    def load_from_file(self, filename="game_logs.json"):
        with open(filename, "r") as file:
            self.logs = json.load(file)