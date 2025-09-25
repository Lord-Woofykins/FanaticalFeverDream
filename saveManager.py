import ast

class SaveManager:
    def __init__(self, fileName="permanentSaveFile.txt"):
        self.fileName = fileName
        
    def saveGameData(self, saveGame):
        try:
            with open(self.fileName, 'w') as file:
                for key, value in saveGame.items():
                    file.write(f"{key} {repr(value)}\n")
        except Exception as error:
            print(f"Error saving game: {error}")
    
    def loadGameData(self):
        # Default values if no save file exists
        defaultData = {
            "playerHealth": 100,
            "playerScore": 0,
            "playerPosition": [550, 550],
            "dungeonMap": {},
            "currentRoom": "1_1",
            "currentRoomPath": {},
            "playerPath": [],
        }
        
        try:
            with open(self.fileName, 'r') as f:
                loadedData = {}
                for line in f:
                    line = line.strip()
                    if line:
                        # Split on first space only
                        parts = line.split(' ', 1)
                        if len(parts) == 2:
                            key, valueStr = parts
                            
                            # Convert string back to appropriate type
                            loadedData[key] = self.parseValue(valueStr)
                
            print(f"Game loaded from {self.fileName}")
            return loadedData
        
        except FileNotFoundError:
            print("No save file found. Using default values.")
            return defaultData
        except Exception as e:
            print(f"Error loading game: {e}. Using default values.")
            return defaultData
    
    def parseValue(self, valueStr):
        """Convert string representation back to original data type"""
        valueStr = valueStr.strip()
        try:
            value = ast.literal_eval(valueStr)
            # Compatibility guard: if value is int but original string contains underscore, return original string
            if isinstance(value, int) and '_' in valueStr:
                return valueStr
            return value
        except:
            return valueStr