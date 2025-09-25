import random

from Platforms import Platform, Door, Transition, Key
from Enemies import GroundEnemy
from ColourPalettes import themeColourPalettes
from RoomLayouts import rooms as roomLayouts

from roomStorage import roomStorage # Required since room gets deleted and rebuilt every so often
from saveFile import saveGame

class Room:
    def __init__(self):
        self.width = 1100
        self.height = 800
        self.theme = "Dungeon"
        self.rows = 16
        self.columns = 22

        self.platforms = []
        self.interactives = []
        self.transitions = []
        self.enemies = []

        self.compatibleConnections = {
            "left": "right",
            "up": "down",
            "right": "left"
        }

        self.startRoom = "1_1"
        self.pullRoomStorage()

        # Pulling Room Data from RoomLayouts
        self.triggers = roomLayouts.get(f"{self.currentRoom}Interactives", {})
        self.roomTransitions = roomLayouts.get(f"{self.currentRoom}Transitions", {})

        self.roomConnections = {}
        for key in roomLayouts:
            if "Transitions" in key:
                try:
                    directions = list(roomLayouts[key].values())  # Get the direction values
                    room = key.replace("Transitions", "")  # Extract room name (e.g., "1_1" from "1_1Transitions")
                    self.roomConnections[room] = directions
                except Exception as error:
                    print(f"{key} failed to provide directions: {error}")

    """
        self.dungeonMapExample = {
            (self.startRoom, "right"): {
                ("1_2", "right"): {
                    ("2_3", "left"): {},
                    },
                ("1_2", "left"): {},
                },
        }

        self.currentRoomPathExample = self.dungeonMapExample[(self.startRoom, "right")][("1_2", "right")]
    """
    def pullRoomStorage(self):
        self.dungeonMap = saveGame["dungeonMap"]
        self.currentRoom = str(saveGame["currentRoom"])
        self.playerPath = saveGame["playerPath"]
    
    def pushRoomStorage(self):
        saveGame["dungeonMap"] = self.dungeonMap
        saveGame["currentRoom"] = str(self.currentRoom)
        saveGame["playerPath"] = self.playerPath

    def retrieveSpawnCoordinates(self, direction, futureRoom):
        # Reverse key value pairs
            directionCoordinateMap = {}
            for key in roomLayouts[f"{futureRoom}Transitions"]:
                directionCoordinateMap[roomLayouts[f"{futureRoom}Transitions"][key]] = key
            
            realDirection = self.compatibleConnections[direction] # Find the direction relevant to the transition (future room perspective)
            # Retrieving player spawn coordinates
            directionCoordinates = directionCoordinateMap[realDirection]
            xSpawn, ySpawn = directionCoordinates

            if realDirection == "left":
                xSpawn += 2
            elif realDirection == "right":
                xSpawn -= 2
            elif realDirection == "up":
                ySpawn += 2
            elif realDirection == "down":
                ySpawn -= 2

            self.currentRoom = futureRoom
            self.pushRoomStorage()
            return futureRoom, xSpawn+1, ySpawn+1

    def generateMapSection(self, direction):
        print("Beginning of generate map dection variables", self.playerPath, self.dungeonMap)
        # Generate room key to determine direction leading there
        currentRoomKey = self.dungeonMap
        for pathKey in self.playerPath:
            currentRoomKey = currentRoomKey[pathKey]
        if len(self.playerPath) >= 1 and self.compatibleConnections[direction] in self.playerPath[-1]: # Check if the next direction is where the user came from
            print("Triggered previous room generation")
            self.playerPath.pop() # Remove last place the player was in

            # Update room path to previous location
            currentRoomKey = self.dungeonMap
            for pathKey in self.playerPath:
                currentRoomKey = currentRoomKey[pathKey]
            
            if self.playerPath:  # only access last element if it exists
                futureRoom, oppositeDirection = self.playerPath[-1] # Find the future room using final tuple in player's path
            else:
                futureRoom, oppositeDirection = self.startRoom, direction
        
        elif len(self.playerPath) >= 1 and direction in currentRoomKey: # Check if the next direction is in one of the next rooms
            print("Trigerred next room generation")
            self.playerPath.append(currentRoomKey) # Add to player's path
            
            # Update room path to previous location
            currentRoomKey = self.dungeonMap
            for pathKey in self.playerPath:
                currentRoomKey = currentRoomKey[pathKey]

            futureRoom, direction = currentRoomKey            
            futureRoom, oppositeDirection = self.playerPath[-1] # Find the future room using final tuple in player's path

        else: # When player ventures into new territory
            """Generating Next Room"""
            # Retrieve all rooms which have correct available directions
            roomOptions = [room for room in self.roomConnections if direction in self.roomConnections[room] and room != self.currentRoom]
            # Choose a room from compatible options
            selectedIndex = random.randint(0, len(roomOptions)-1)
            futureRoom = roomOptions[selectedIndex]

            """Logging room changes"""

            # Create tuple to log path
            futureTuple = (self.currentRoom, direction)

            # Keep a log of the path the player has taken in list form
            self.playerPath.append(futureTuple)
            
            # Find path to current room (value)
            currentRoomKey = self.dungeonMap # Derive overall map
            for pathKey in self.playerPath: # Go through all previous directions taken
                if pathKey not in currentRoomKey:
                    currentRoomKey[pathKey] = {} # create empty dict if missing
                currentRoomKey = currentRoomKey[pathKey]

            currentRoomKey[futureTuple] = {} # Add room to dungeon map
            
            print(f"Dungeon map: {self.dungeonMap}, Player path: {self.playerPath}")
        
        return self.retrieveSpawnCoordinates(direction, futureRoom)
            
    def loadRoom(self):
        """Load the room layout and create platforms"""
        # Clear Existing Room Data
        self.platforms = []
        self.interactives = []
        self.transitions = []
        
        flatLayout = roomLayouts[self.currentRoom]
        layout = [flatLayout[i*self.columns:(i+1)*self.columns] for i in range(0, self.rows)] # Converts one long list into a list(y) of lists(x)

        interactiveMap = {}
        for y in range(0, self.rows):
            for x in range(0, self.columns):
                cellVal = layout[y][x]
                xPos, yPos = x * 50, y * 50
                rectWidth, rectHeight = 50, 50

                # Creating and mapping transitions
                directionData = self.roomTransitions.get((x, y))   # Get transition data for this cell
                if directionData:
                    transitionObj = Transition(xPos, yPos, rectWidth, rectHeight, "transition", directionData, self.theme, self.generateMapSection)
                    self.transitions.append(transitionObj)

                if cellVal == 1:
                    platformObj = Platform(xPos, yPos, rectWidth, rectHeight, "platform", self.theme)
                    self.platforms.append(platformObj)
                elif cellVal == 2:
                    # Adjust door dimensions in case door is on top or bottom
                    if y == 0 or y == 15:
                        rectWidth += 50
                    else:
                        rectHeight += 50
                    doorObj = Door(xPos, yPos, rectWidth, rectHeight, "closedDoor", self.theme)
                    self.platforms.append(doorObj)
                    interactiveMap[(x, y)] = doorObj
                elif int(cellVal/10) == 2:
                    if cellVal - 20 == 1:
                        direction = 1
                    elif cellVal - 20 == 2:
                        direction = -1
                    enemyObj = GroundEnemy(x*50, y*50, 40, 60, 2, direction, 4*50, 10, themeColourPalettes[self.theme]["groundEnemy"]) # xPos, yPos, width, height, speed, direction, patrolRange, damage, colour
                    self.enemies.append(enemyObj)


        # Second loop for interacrtives relying on other objects created first
        for y in range(0, self.rows):
            for x in range(0, self.columns):
                cellVal = layout[y][x]
                xPos, yPos = x * 50, y * 50
                rectWidth, rectHeight = 50, 50
                if cellVal == 10:
                    targetCoordinates = self.triggers.get((x, y))
                    targetInteractive = interactiveMap.get(targetCoordinates)
                    keyObj = Key(xPos, yPos, rectWidth, rectHeight, "key", targetInteractive, self.theme)
                    self.interactives.append(keyObj)
    
    def draw(self, camera, screen):
        # Draw background
        backgroundColour = themeColourPalettes[self.theme]["background"]
        screen.fill(backgroundColour)

        # Draw platforms with camera offset
        for platform in self.platforms:
            platform.draw(camera)
        for object in self.interactives:
            object.draw(camera)