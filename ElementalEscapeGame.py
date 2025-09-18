import pygame as py
from RoomLayouts import rooms as roomLayouts
import sys

# Import classes form other files
from Enemy import GroundEnemy

py.init() # Initialize Pygame Modules

# Constants
GREEN = (0, 128, 0)

# Setting Up Window
WIDTH, HEIGHT = 1100, 800

FRAMETIME = 60

GRAVITY = 0.5

ACCELERATION = 1
DECELERATION = 2
maxSpeed = 8
standSpeed = 8
crouchSpeed = 3

JUMPFORCE = 10.5    

nameOfGame = "Roguelike Shapeshifter"

py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption(nameOfGame)
screen = py.display.get_surface()

py.mouse.set_visible(False)

clock = py.time.Clock()

startingPosition = [100, 800]

class Player:
    def __init__(self, width=40, height=70):
        self.position = startingPosition.copy()
        self.width = width
        self.height = height

        self.standHeight = height
        self.crouchHeight = min(50, height/2) # Dynamic height adjustment for changing later

        self.yVelocity = 0
        self.xVelocity = 0

        self.onGround = False

    def movePlayer(self, xAcceleration):
        self.xVelocity += xAcceleration
        self.xVelocity = max(-maxSpeed, min(self.xVelocity, maxSpeed)) # Limit horizontal speed by: max(absolute minimum, actual speed capped at maximum)-> restricted velocity

        if xAcceleration == 0:
            if self.xVelocity > 0:
                self.xVelocity = max(0, self.xVelocity - DECELERATION)
            elif self.xVelocity < 0:
                self.xVelocity = min(0, self.xVelocity + DECELERATION)
    
    def crouch(self):
        self.height = self.crouchHeight
        self.position[1] += self.height / 2 # Adjusting position to stay grounded
        global maxSpeed
        maxSpeed = crouchSpeed
        
    def stand(self):
        self.height = self.standHeight
        self.position[1] -= self.crouchHeight / 2 # Adjusting position to normal height
        global maxSpeed
        maxSpeed = standSpeed
        
    def jump(self):
        if self.onGround:  # Only jump if on ground
            self.yVelocity = -JUMPFORCE

    def updateGravity(self):
        self.yVelocity += GRAVITY

    def getRect(self):
        return py.Rect(self.position[0] - (self.width / 2), self.position[1] - (self.height / 2), 
        self.width, self.height)

    def draw(self, camera):
        # Create a rect for the player in world coordinates
        playerRect = py.Rect(self.position[0] - self.width/2, self.position[1] - self.height/2, self.width, self.height)
        # Apply camera offset and zoom to the entire rectangle
        screenRect = camera.applyRect(playerRect)
        py.draw.rect(screen, GREEN, screenRect)



class Camera:
    def __init__(self, zoom=1.4):
        self.x = 0
        self.y = 0
        self.xTarget = 0
        self.yTarget = 0
        self.smoothing = 0.6  # Lower = smoother, higher = more responsive
        self.zoom = zoom
        
        # Calculate effective screen size
        self.viewWidth = WIDTH / self.zoom
        self.viewHeight = HEIGHT / self.zoom
    
    def follow(self, xTarget, yTarget):
        # Calculate where the camera should be to center the target (accounting for zoom)
        self.xTarget = xTarget - self.viewWidth // 2
        self.yTarget = yTarget - self.viewHeight // 2
        
        # Smooth camera movement
        self.x += (self.xTarget - self.x) * self.smoothing
        self.y += (self.yTarget - self.y) * self.smoothing
        
        # Constrain camera to room bounds (accounting for zoom)
        roomWidth = room.columns * 50
        roomHeight = room.rows * 50
        
        self.x = max(0, min(self.x, roomWidth - self.viewWidth))
        self.y = max(0, min(self.y, roomHeight - self.viewHeight))
    
    def apply(self, x, y):
        """Convert world coordinates to screen coordinates with zoom"""
        xScreen = (x - self.x) * self.zoom
        yScreen = (y - self.y) * self.zoom
        return int(xScreen), int(yScreen)
    
    def applyRect(self, rect):
        """Apply camera offset and zoom to a rectangle"""
        xScreen = (rect.x - self.x) * self.zoom
        yScreen = (rect.y - self.y) * self.zoom
        screenWidth = rect.width * self.zoom
        screenHeight = rect.height * self.zoom
        return py.Rect(xScreen, yScreen, screenWidth, screenHeight)

class Platform:
    def __init__(self, x, y, width, height, platformType):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.platformType = platformType
    
    def getRect(self):
        return py.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, camera):
        # Only draw if platform is visible on screen (with zoom consideration)
        screenRect = camera.applyRect(self.getRect())
        if (screenRect.right > -screenRect.width and screenRect.left < WIDTH + screenRect.width and 
            screenRect.bottom > -screenRect.height and screenRect.top < HEIGHT + screenRect.height):
            platformColour = themeColourPalettes[room.theme][self.platformType]
            py.draw.rect(screen, platformColour, screenRect)

class Door(Platform):
    def __init__(self, x, y, width, height, platformType):
        super().__init__(x, y, width, height, platformType)
        self.isOpen = False

    def trigger(self):
        self.isOpen = True
        self.platformType = "openDoor"

class Transition(Platform):
    def __init__(self, x, y, width, height, platformType, targetRoom, playerSpawnX, playerSpawnY):
        super().__init__(x, y, width, height, platformType)
        self.targetRoom = targetRoom
        self.playerSpawnX = playerSpawnX
        self.playerSpawnY = playerSpawnY

    def trigger(self, gameManager):
        gameManager.changeRoom(self.targetRoom, self.playerSpawnX*50, self.playerSpawnY*50)

class Key(Platform):
    def __init__(self, x, y, width, height, platformType, targetInteractive):
        super().__init__(x, y, width, height, platformType)
        self.triggered = False
        self.targetInteractive = targetInteractive

    def trigger(self):
        if not self.triggered:
            self.triggered = True
            self.targetInteractive.trigger()


themeColourPalettes = {
    "Forest": {
        "background": (34, 139, 34),
        "platform": (139, 69, 19),
        "door": (164, 116, 73),
    },
    "Dungeon": {
        "background": (100, 110, 120),
        "platform": (100, 120, 140),
        "closedDoor": (129,97,62),
        "openDoor": (129,97,62, 50),
        "key": (203,161,53),
        "transition": (255, 50, 100),
        "groundEnemy": (150, 0, 0),
    }, 
}

class Room:
    def __init__(self, currentRoom="cell", theme="Dungeon"):
        self.width = WIDTH
        self.height = HEIGHT
        self.currentRoom = currentRoom
        self.theme = theme
        self.rows = 16
        self.columns = 22

        self.platforms = []
        self.interactives = []
        self.transitions = []
        self.enemies = []

        # Pulling Room Data from RoolLayouts
        self.triggers = roomLayouts.get(f"{currentRoom}Interactives", {})
        self.roomTransitions = roomLayouts.get(f"{currentRoom}Transitions", {})
        
    def loadRoom(self):
        """Load the room layout and create platforms"""
        # Clear Exxisting Room Data
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
                if transitionData:                                  # Check if transitions exist
                    targetRoom, spawnX, spawnY = transitionData
                    transitionObj = Transition(xPos, yPos, rectWidth, rectHeight, "transition", targetRoom, spawnX, spawnY)
                    self.transitions.append(transitionObj)

                if cellVal == 1:
                    platformObj = Platform(xPos, yPos, rectWidth, rectHeight, "platform")
                    self.platforms.append(platformObj)
                elif cellVal == 2:
                    doorObj = Door(xPos, yPos, rectWidth, rectHeight+50, "openDoor")
                    self.platforms.append(doorObj)
                    interactiveMap[(x, y)] = doorObj
                elif int(cellVal/10) == 2:
                    if cellVal - 20 == 1:
                        direction = 1
                    elif cellVal - 20 == 2:
                        direction = -1
                    enemyObj = GroundEnemy(x*50, y*50, 40, 60, 2, direction, 4*50, themeColourPalettes[self.theme]["groundEnemy"]) # xPos, yPos, width, height, speed, direction, patrolRange
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
                    keyObj = Key(xPos, yPos, rectWidth, rectHeight, "key", targetInteractive)
                    self.interactives.append(keyObj)
                    
    def draw(self, camera):
        # Draw background
        backgroundColour = themeColourPalettes[self.theme]["background"]
        screen.fill(backgroundColour)
        
        # Draw platforms with camera offset
        for platform in self.platforms:
            platform.draw(camera)
        for object in self.interactives:
            object.draw(camera)

class GameManager:
    def __init__(self, player):
        self.currentRoom = None
        self.player = player
        
    def changeRoom(self, futureRoom, playerX, playerY):
        """Change to a new room and position the player"""
        print(f"Changing to room: {futureRoom}")
        print(f"Spawning player at: ({playerX}, {playerY})")
        
        # Create and load the new room
        self.currentRoom = Room(futureRoom)
        self.currentRoom.loadRoom()
        
        # Position the player at the spawn point
        self.player.position[0] = playerX
        self.player.position[1] = playerY
        
        # Reset player physics
        self.player.xVelocity = 0
        self.player.yVelocity = 0

        camera.follow(playerX, playerY)

        self.transitionFade()

    def transitionFade(self):
        fadeSurface = py.Surface((WIDTH, HEIGHT), py.SRCALPHA)
        fadeSteps = 20  # increasing this value decreases fade speed

        # Fade out
        for step in range(fadeSteps + 1):
            alpha = int((step / fadeSteps) * 255)

            # create a sudo game loop while fade occurs ro process essential changes
            self.currentRoom.draw(camera)
            self.player.draw(camera)
            # overlay with alpha
            fadeSurface.fill((0, 0, 0, alpha))
            screen.blit(fadeSurface, (0, 0))
            py.display.flip()

            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
            clock.tick(FRAMETIME)

        # Fade in
        for i in range(fadeSteps + 1):
            alpha = int(((fadeSteps - i) / fadeSteps) * 255)
            self.currentRoom.draw(camera)
            self.player.draw(camera)
            fadeSurface.fill((0, 0, 0, alpha))
            screen.blit(fadeSurface, (0, 0))
            py.display.flip()

            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
            clock.tick(FRAMETIME)
        

class CollisionManager:
    def handleCollisions(self, player, room):
        # Apply vertical movement first
        player.position[1] += player.yVelocity
        playerRect = player.getRect()
        
        # Check for vertical collisions
        for platform in room.platforms:
            if platform.platformType == "openDoor" and platform.isOpen:
                continue
            platRect = platform.getRect()
            if playerRect.colliderect(platRect):
                if player.yVelocity > 0:  # Falling down - landed on platform
                    player.position[1] = platform.y - player.height / 2
                    player.yVelocity = 0
                elif player.yVelocity < 0:  # Moving up - hit ceiling
                    player.position[1] = platform.y + platform.height + player.height / 2
                    player.yVelocity = 0
                break

        # Apply horizontal movement
        player.position[0] += player.xVelocity
        playerRect = player.getRect()
        
        # Check horizontal collisions
        for platform in room.platforms:
            if platform.platformType == "openDoor" and platform.isOpen:
                continue
            platRect = platform.getRect()
            if playerRect.colliderect(platRect):
                if player.xVelocity > 0:  # Moving right
                    player.position[0] = platform.x - player.width / 2
                elif player.xVelocity < 0:  # Moving left
                    player.position[0] = platform.x + platform.width + player.width / 2
                player.xVelocity = 0
                break

        # Check if player is on ground (separate check after movement)
        player.onGround = False
        groundCheckRect = py.Rect(player.position[0] - player.width/2, player.position[1] + player.height/2, player.width, 2)  # Small rect below player
        
        for platform in room.platforms:
            if groundCheckRect.colliderect(platform.getRect()):
                player.onGround = True
                break
    
    def handleInteractions(self, player, room, gameManager):
        playerRect = player.getRect()

        # Handle regular interactives (keys, etc.)
        for object in room.interactives:
            objectRect = object.getRect()
            if playerRect.colliderect(objectRect):
                try:
                    object.trigger()
                except AttributeError:
                    print("Interactive Failed To Trigger")
                    continue

        # Handle room transitions
        for transition in room.transitions:
            transitionRect = transition.getRect()
            if playerRect.colliderect(transitionRect):
                try:
                    transition.trigger(gameManager)
                except:
                    print("Transition Failed To Trigger")
                    continue

    def checkEnemyCollisions(self, player, enemies):
        playerRect = player.getRect()
        for enemy in enemies:
            enemyRect = py.Rect(enemy.position[0] - enemy.width/2, enemy.position[1] - enemy.height/2, enemy.width, enemy.height)
            if playerRect.colliderect(enemyRect):
                pass



# Create game objects
mainCharacter = Player()
gameManager = GameManager(mainCharacter)
gameManager.currentRoom = Room()
gameManager.currentRoom.loadRoom() # load room from game manager

# For compatibility with existing code
room = gameManager.currentRoom

collisionManager = CollisionManager()
camera = Camera()

"""Main game loop"""
running = True
while running:
    # Keep the room reference to that in the game manager
    room = gameManager.currentRoom
    
    # Handle events
    for event in py.event.get():
        # Quit game
        if event.type == py.QUIT:
            running = False
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                running = False
        # Movement events
            if event.key == py.K_s:
                mainCharacter.crouch()
            if event.key == py.K_DOWN:
                mainCharacter.crouch()
            if event.key == py.K_w:
                mainCharacter.jump()
            if event.key == py.K_UP:
                mainCharacter.jump()
        if event.type == py.KEYUP:
            if event.key == py.K_s:
                mainCharacter.stand()
            if event.key == py.K_DOWN:
                mainCharacter.stand()
    
    # Handle continuous input
    keys = py.key.get_pressed()
    if keys[py.K_a] or keys[py.K_d]:
        if keys[py.K_a]:
            mainCharacter.movePlayer(-ACCELERATION)
        elif keys[py.K_d]:
            mainCharacter.movePlayer(ACCELERATION)
    elif keys[py.K_LEFT] or keys[py.K_RIGHT]:
        if keys[py.K_LEFT]:
            mainCharacter.movePlayer(-ACCELERATION)
        elif keys[py.K_RIGHT]:
            mainCharacter.movePlayer(ACCELERATION)
    else:
            mainCharacter.movePlayer(0)  # Stop horizontal movement if no input

    # Update physics
    mainCharacter.updateGravity()
    collisionManager.handleCollisions(mainCharacter, room)

    # Process interactions
    collisionManager.handleInteractions(mainCharacter, room, gameManager)
    
    # Update camera to follow player
    camera.follow(mainCharacter.position[0], mainCharacter.position[1])
    print(f"Camera Position: ({camera.x:.2f}, {camera.y:.2f})")
    print(f"Player Position: ({mainCharacter.position[0]:.2f}, {mainCharacter.position[1]:.2f})")
    
    # Draw game for player
    room.draw(camera)
    mainCharacter.draw(camera)

    # Update and draw enemies
    for enemy in room.enemies:
        enemy.patrol()
        enemy.draw(camera)
        collisionManager.checkEnemyCollisions(mainCharacter, room.enemies)

    # Update the display
    py.display.flip()
    clock.tick(FRAMETIME)

py.quit()