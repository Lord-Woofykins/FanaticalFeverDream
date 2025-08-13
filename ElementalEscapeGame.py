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
        selfRect = self.getRect()
        for platform in room.platforms:
            platRect = platform.getRect()
            if selfRect.colliderect(platRect):
                self.yVelocity = -10
                print(self.yVelocity)



    def updateGravity(self):
        # Apply gravity
        self.yVelocity += GRAVITY

    def getRect(self):
        x, y = self.position
        return py.Rect(x - (self.width / 2), y - (self.height / 2), self.width, self.height)

    def draw(self):
        x, y = self.position
        py.draw.rect(screen, GREEN, ((x - (self.width/2)), (y - (self.height/2)), self.width, self.height))
    
mainCharacter = Player("Player1")
mainCharacter.draw()


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
    def __init__(self):
        self.platforms = room.platforms

    def handle_collisions(self, player):
        # Vertical collision
        player.position = (player.position[0], player.position[1] + player.yVelocity)
        player_rect = player.getRect()
        for platform in self.platforms:
            plat_rect = platform.getRect()

            if player_rect.colliderect(plat_rect):
                if player.yVelocity > 0:
                    # Landing on top
                    player.position = (player.position[0], platform.y - player.height / 2)
                    print("triggered top")
                    print(platform.y)

                elif player.yVelocity < 0:
                    # Hitting head
                    player.position = (player.position[0], platform.y + platform.height + player.height / 2)
                player.yVelocity = 0
                player_rect = player.getRect()  # Update rect after position change

        # Horizontal collision
        player.position = (player.position[0] + player.xVelocity, player.position[1])
        player_rect = player.getRect()
        for platform in self.platforms:
            plat_rect = platform.getRect()
            if player_rect.colliderect(plat_rect):
                if player.xVelocity > 0:
                    # Hitting wall on right
                    player.position = (platform.x - player.width / 2, player.position[1])
                    print("triggered right")
                elif player.xVelocity < 0:
                    # Hitting wall on left
                    player.position = (platform.x + platform.width + player.width / 2, player.position[1])
                    print("triggered left")
                player.xVelocity = 0
                player_rect = player.getRect()  # Update rect after position change
collision_manager = CollisionManager()

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
            if event.key == py.K_ESCAPE:
                running = False
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

    # Player updates per frame

    # Movement updates
    mainCharacter.updateGravity() # Apply gravity
    collision_manager.handle_collisions(mainCharacter) # Resolve collisions

    # Other updates


    mainCharacter.draw() # Draw/show changes

    
    py.display.update()


py.quit()
