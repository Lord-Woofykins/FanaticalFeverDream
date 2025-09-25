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

        self.initialDungeonMap = {}
        self.startRoom = "1_1"
        self.pullRoomStorage()

        # Pulling Room Data from RoomLayouts
        self.triggers = roomLayouts.get(f"{self.currentRoom}Interactives", {})
        self.roomTransitions = roomLayouts.get(f"{self.currentRoom}Transitions", {})

        self.roomConnections = {}
        for key in roomLayouts:
            if "Transitions" in key:
                try:
                    print(key)
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
        self.currentRoomPath = saveGame["currentRoomPath"]
        self.playerPath = saveGame["playerPath"]
    
    def pushRoomStorage(self):
        saveGame["dungeonMap"] = self.dungeonMap
        saveGame["currentRoom"] = str(self.currentRoom)
        saveGame["currentRoomPath"] = self.currentRoomPath
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
            return futureRoom, xSpawn, ySpawn

    def generateMapSection(self, direction):
        if len(self.playerPath) >= 1 and self.compatibleConnections[direction] in self.playerPath[-1]: # Check if the next direction is where the user came from
            print("Triggered previous room generation")
            self.playerPath.pop() # Remove last place the player was in

            # Update room path to previous location
            self.currentRoomPath = self.initialDungeonMap
            for pathKey in self.playerPath:
                self.currentRoomPath = self.currentRoomPath[pathKey]
            
            futureRoom, oppositeDirection = self.playerPath[-1] # Find the future room using final tuple in player's path
        
        elif self.compatibleConnections[direction] in self.currentRoomPath:
            self.playerPath.append(self.currentRoomPath)
            
            # Update room path to previous location
            self.currentRoomPath = self.initialDungeonMap
            for pathKey in self.playerPath:
                self.currentRoomPath = self.currentRoomPath[pathKey]
            
            futureRoom, oppositeDirection = self.playerPath[-1] # Find the future room using final tuple in player's path

        else:
            # Retrieve all rooms which have correct available directions
            roomOptions = [room for room in self.roomConnections if direction in self.roomConnections[room] and room != self.currentRoom]
            selectedIndex = random.randint(0, len(roomOptions)-1)
            futureRoom = roomOptions[selectedIndex]


            futureTuple = (self.currentRoom, direction)
            if not self.dungeonMap:
                    self.dungeonMap[futureTuple] = {}
                    self.currentRoomPath = self.dungeonMap[futureTuple]
            else:
                    # Add new room inside the current path
                    self.currentRoomPath[futureTuple] = {}
                    self.currentRoomPath = self.currentRoomPath[futureTuple]  # move pointer into nested dict

            self.playerPath.append(futureTuple)
            print(self.dungeonMap)

            self.playerPath.append(futureTuple)
        
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