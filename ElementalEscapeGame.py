import pygame as py
from RoomLayouts import rooms as roomLayouts

py.init() # Initialize Pygame Modules

# Constants
GREEN = (0, 128, 0)

# Setting Up Window
WIDTH, HEIGHT = 1100, 800

GRAVITY = 0.5

ACCELERATION = 1
DECELERATION = 2
maxSpeed = 8

nameOfGame = "Roguelike Shapeshifter TEST"

py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption(nameOfGame)
screen = py.display.get_surface()

py.mouse.set_visible(False)

clock = py.time.Clock()

startingPosition = [400, 600]

crouchHeight = 25
standHeight = 50
class Player:
    def __init__(self, width=40, height=50):
        self.position = startingPosition
        self.width = width
        self.height = height

        self.yVelocity = 0
        self.xVelocity = 0

        self.crouchToggled = False
        self.onGround = False

        print(f"Player {self.name} created at position {self.position}")

    def movePlayer(self, xAcceleration):
        self.xVelocity += xAcceleration
        self.xVelocity = max(-maxSpeed, min(self.xVelocity, maxSpeed)) # Limit horizontal speed by: max(absolute minimum, actual speed capped at maximum)-> restricted velocity

        if xAcceleration == 0:
            if self.xVelocity > 0:
                self.xVelocity = max(0, self.xVelocity - DECELERATION)
            elif self.xVelocity < 0:
                self.xVelocity = min(0, self.xVelocity + DECELERATION)
    
    def crouch(self):
        oldHeight = self.height
        self.height = crouchHeight
        # Adjust position to keep player on ground when crouching
        print(self.position[1])
        self.position[1] += (oldHeight - self.height) / 2
        
    def stand(self):
        old_height = self.height
        self.height = standHeight
        # Adjust position to keep player on ground when standing
        self.position[1] -= (self.height - old_height) / 2
        
    def jump(self):
        if self.onGround:  # Only jump if on ground
            self.yVelocity = -12

    def updateGravity(self):
        self.yVelocity += GRAVITY

    def getRect(self):
        return py.Rect(self.position[0] - (self.width / 2), self.position[1] - (self.height / 2), 
        self.width, self.height)

    def draw(self):
        py.draw.rect(screen, GREEN, (self.position[0] - (self.width/2), self.position[1] - (self.height/2), self.width, self.height))

class Platform:
    def __init__(self, x, y, width=50, height=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def getRect(self):
        return py.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self):
        platformColour = themeColourPalettes[room.theme]["platform"]
        py.draw.rect(screen, (platformColour), self.getRect())

themeColourPalettes = {
    "Forest": {
        "background": (34, 139, 34),
        "platform": (139, 69, 19),
    },
    "Dungeon": {
        "background": (100, 120, 140),
        "platform": (139, 69, 19),
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
        
    def loadRoom(self):
        """Load the room layout and create platforms"""
        self.platforms = []  # Clear existing platforms
        
        flatLayout = roomLayouts[self.currentRoom]
        layout = [flatLayout[i*self.columns:(i+1)*self.columns] for i in range(0, self.rows)] # Converts one long list into a list of lists

        for y in range(0, self.rows):
            for x in range(0, self.columns):
                if layout[y][x] == 1:
                    xPos, yPos = x * 50, y * 50
                    rectWidth, rectHeight = 50, 50
                    platformObj = Platform(xPos, yPos, rectWidth, rectHeight)
                    self.platforms.append(platformObj)
    
    def draw(self):
        # Draw background
        screen.fill((50, 50, 50))
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw()

class CollisionManager:
    def handle_collisions(self, player, room):
        # Apply vertical movement first
        player.position[1] += player.yVelocity
        playerRect = player.getRect()
        
        # Check for vertical collisions
        for platform in room.platforms:
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

# Create game objects
mainCharacter = Player()
room = Room()
room.loadRoom()
collision_manager = CollisionManager()

# Main game loop
running = True
while running:
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
            if event.key == py.K_w:
                mainCharacter.jump()
        if event.type == py.KEYUP:
            if event.key == py.K_s:
                mainCharacter.stand()
    
    # Handle continuous input
    keys = py.key.get_pressed()
    if keys[py.K_a]:
        mainCharacter.movePlayer(-ACCELERATION)
    elif keys[py.K_d]:
        mainCharacter.movePlayer(ACCELERATION)
    else:
        mainCharacter.movePlayer(0)  # Stop horizontal movement if no input

    # Update physics
    mainCharacter.updateGravity()
    collision_manager.handle_collisions(mainCharacter, room)
    
    # Draw game for player
    room.draw()
    mainCharacter.draw()
    
    # Update the display
    py.display.flip()
    clock.tick(60)

py.quit()