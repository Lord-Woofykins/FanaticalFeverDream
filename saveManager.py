class SaveManager:
    def __init__(self, fileName="permanentSaveFile.txt"):
        self.fileName = fileName
        
    def saveGameData(self, saveGame):
        try:
            with open(self.fileName, 'w') as file:
                for key, value in saveGame.items():
                    file.write(f"{key} {value}\n")
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
        
        # Handle lists [550, 550] or []
        if valueStr.startswith('[') and valueStr.endswith(']'):
            try:
                # Use eval for simple lists (be careful with this in production!)
                return eval(valueStr)
            except:
                return []
        
        # Handle dictionaries {} 
        if valueStr.startswith('{') and valueStr.endswith('}'):
            try:
                return eval(valueStr) if valueStr != '{}' else {}
            except:
                return {}
        
        # Handle integers
        try:
            return int(valueStr)
        except ValueError:
            pass
        
        # Handle floats
        try:
            return float(valueStr)
        except ValueError:
            pass
        
        # Return as string
        return valueStr