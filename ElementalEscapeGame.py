import pygame as py
from RoomLayouts import rooms as roomLayouts

py.init() # Initialize Pygame Modules

# Constants
GREEN = (0, 128, 0)

# Setting Up Window
WIDTH, HEIGHT = 1100, 800

GRAVITY = 0.5
GROUND_HEIGHT = 725

ACCELERATION = 1
DECELERATION = 2
maxSpeed = 8

nameOfGame = "Roguelike Shapeshifter TEST"

py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption(nameOfGame)
screen = py.display.get_surface()

clock = py.time.Clock()

currentRoom = "cell"

startingPosition = (400, 600)

crouchHeight = 25
standHeight = 50


class Player:
    def __init__(self, name, width=40, height=50):
        self.name = name
        self.position = startingPosition
        self.width = width
        self.height = height

        self.yVelocity = 0
        self.xVelocity = 0

        self.crouchToggled = False

        print(f"Player {self.name} created at position {self.position}")

    def movePlayer(self, xAcceleration):
        self.xVelocity += xAcceleration
        self.xVelocity = max(-maxSpeed, min(self.xVelocity, maxSpeed))  # Limit horizontal speed by: max(absolute minimum, actual speed capped at maximum)-> restricted velocity
        #print(self.xVelocity, end=' ', flush=True)
        x, y = self.position
        future_x = x + self.xVelocity

        # Check for screen boundaries
        if future_x < (0 + self.width / 2):
            future_x = (0 + self.width / 2)
        elif future_x > (WIDTH - (self.width / 2)):
            future_x = (WIDTH - (self.width / 2))
        
        self.position = (future_x, y)

        if xAcceleration == 0:
            if self.xVelocity > 0:
                self.xVelocity -= DECELERATION
            elif self.xVelocity < 0:
                self.xVelocity += DECELERATION
    
    def crouch(self):
        self.height = crouchHeight
    def stand(self):
        self.height = standHeight
    def jump(self):
        platformsList = [Platform(*p) for p in platforms]
        selfRect = self.getRect()
        for platform in platformsList:
            selfRect = platform.getRect()
            if selfRect.colliderect(selfRect):
                self.yVelocity = -10
                print(self.yVelocity)



    def updateGravity(self):
        # Apply gravity
        self.yVelocity += GRAVITY
        x, y = self.position
        y += self.yVelocity

        # Check for ground collision
        if y >= GROUND_HEIGHT:
            y = GROUND_HEIGHT
            self.yVelocity = 0  # Reset vertical velocity on ground contact
        
        self.position = (x, y)

    def getRect(self):
        x, y = self.position
        return py.Rect(x - (self.width / 2), y - (self.height / 2), self.width, self.height)

    def draw(self):
        x, y = self.position
        py.draw.rect(screen, GREEN, ((x - (self.width/2)), (y - (self.height/2)), self.width, self.height))
    
mainCharacter = Player("Player1")
mainCharacter.draw()




platforms = [
    # Tuple of (x, y, width, height)
    (0, GROUND_HEIGHT+25, WIDTH, 50),
    (100, GROUND_HEIGHT-50, 200, 50),
    (400, GROUND_HEIGHT-100, 200, 50),
    (700, GROUND_HEIGHT-150, 200, 50),
    (900, GROUND_HEIGHT-200, 200, 50),
    (300, GROUND_HEIGHT-250, 200, 50),
    (600, GROUND_HEIGHT-300, 200, 50),
    (800, GROUND_HEIGHT-350, 200, 50)
]

class Platform():
    def __init__(self, x, y, width=50, height=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def getRect(self):
        return py.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self):
        py.draw.rect(screen, (100, 100, 100), self.getRect())


themeColourPalettes = {
    "Dungeon": (100, 120, 140)
}

class Room():
    def __init__(self, currentRoom="Cell", theme="Dungeon"):
        self.width = WIDTH
        self.height = HEIGHT
        self.currentRoom = currentRoom
        self.theme = theme
        self.rows = 16
        self.columns = 22
        self.platforms = []
        
    
    def draw(self):
        flatLayout = roomLayouts[self.currentRoom]
        layout = [flatLayout[i*self.columns:(i+1)*self.columns] for i in range(self.rows)] # Converts one long list into a list of lists

        for y in range(0, self.rows):
            for x in range(0, self.columns):
                if layout[y][x] == 1:
                    xPos, yPos, rectWidth, rectHeight = (x*50, y*50, WIDTH//self.columns, HEIGHT//self.rows)
                    py.draw.rect(screen, (themeColourPalettes[self.theme]), (xPos, yPos, rectWidth, rectHeight))
                    platformObj = Platform(xPos, yPos, rectWidth, rectHeight)
                    platformObj.draw()
                    self.platforms.append(platformObj)

            
            
            
    
    def updateLayout():
        pass

room = Room()
class CollisionManager:
    def __init__(self, player):
        self.player = player
        self.platforms = room.platforms

    def handle_collisions(self):
        player_rect = self.player.getRect()
        for platform in self.platforms:
            plat_rect = platform.getRect()
            if player_rect.colliderect(plat_rect):
                self.resolve_collision(platform)

    def resolve_collision(self, platform):
        # Y axis colision logic
        if self.player.yVelocity > 0:
            # Top collision
            self.player.position = (self.player.position[0], platform.y - self.player.height / 2)
            self.player.yVelocity = 0
        elif self.player.yVelocity < 0:
            # Bottom collision
            self.player.position = (self.player.position[0], platform.y + platform.height + self.player.height / 2)
            self.player.yVelocity = 0
        # X axis collision logic
        if self.player.xVelocity > 0:
            # Left collision
            self.player.position = (platform.x - self.player.width / 2, self.player.position[1])
            self.player.xVelocity = 0
        elif self.player.xVelocity < 0:
            # Left collision
            self.player.position = (platform.x + platform.width + self.player.width / 2, self.player.position[1])
            self.player.xVelocity = 0


        # Horizontal collision (optional, for walls)
        # You can add similar logic for left/right collisions if needed

collision_manager = CollisionManager(mainCharacter)

running = True
while running:

    # Prepare the screen for next frame
    screen.fill((0, 0, 0))  # Clear the screen
    clock.tick(60) # Limit the frame rate to 60 FPS

    # Respond to player input
    for event in py.event.get():
        # Quit the game
        if event.type == py.QUIT:
            running = False
        if event.type == py.KEYDOWN:
            if event.key == py.K_s:
                mainCharacter.crouch()
            if event.key == py.K_w:
                mainCharacter.jump()
        if event.type == py.KEYUP:
            if event.key == py.K_s:
                mainCharacter.stand()
    
    keys = py.key.get_pressed()
    if keys[py.K_a] or keys[py.K_d]:
        if keys[py.K_a]:
            mainCharacter.movePlayer(-ACCELERATION)  # Move left
        if keys[py.K_d]:
            mainCharacter.movePlayer(ACCELERATION)
    else:
        mainCharacter.movePlayer(0)  # Stop horizontal movement if no input
        
    room.draw()

    mainCharacter.updateGravity()
    collision_manager.handle_collisions()
    mainCharacter.draw()

    
    py.display.update()


py.quit()
