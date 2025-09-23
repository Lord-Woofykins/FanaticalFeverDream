from Platforms import Platform, Door, Transition, Key
from Enemies import GroundEnemy
from ColourPalettes import themeColourPalettes
from RoomLayouts import rooms as roomLayouts

class Room:
    def __init__(self, currentRoom="1_1", theme="Dungeon"):
        self.width = 1100
        self.height = 800
        self.currentRoom = currentRoom
        self.theme = theme
        self.rows = 16
        self.columns = 22

        self.platforms = []
        self.interactives = []
        self.transitions = []
        self.enemies = []

        # Pulling Room Data from RoomLayouts
        self.triggers = roomLayouts.get(f"{currentRoom}Interactives", {})
        self.roomTransitions = roomLayouts.get(f"{currentRoom}Transitions", {})

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
                transitionData = self.roomTransitions.get((x, y))   # Get transition data for this cell
                if transitionData:  
                    break
                    ### Convert direction to room
                    targetRoom, spawnX, spawnY = transitionData
                    transitionObj = Transition(xPos, yPos, rectWidth, rectHeight, "transition", targetRoom, spawnX, spawnY, self.theme)
                    self.transitions.append(transitionObj)

                if cellVal == 1:
                    platformObj = Platform(xPos, yPos, rectWidth, rectHeight, "platform", self.theme)
                    self.platforms.append(platformObj)
                elif cellVal == 2:
                    doorObj = Door(xPos, yPos, rectWidth, rectHeight+50, "openDoor", self.theme)
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