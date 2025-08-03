import pygame as py

py.init() # Initialize Pygame Modules

# Constants
GREEN = (0, 128, 0)

# Setting Up Window
WIDTH, HEIGHT = 1100, 800

GRAVITY = 0.5
GROUND_HEIGHT = 725

ACCELERATION = 1
DECELERATION = 2
max_speed = 8

nameOfGame = "Roguelike Shapeshifter TEST"

py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption(nameOfGame)
screen = py.display.get_surface()

clock = py.time.Clock()

startingPosition = (400, 600)

class Player:
    def __init__(self, name, width=50, height=50):
        self.name = name
        self.position = startingPosition
        self.width = width
        self.height = height

        self.velocity_y = 0
        self.velocity_x = 0

        print(f"Player {self.name} created at position {self.position}")

    def movePlayer(self, acceleration_x):
        self.velocity_x += acceleration_x
        self.velocity_x = max(-max_speed, min(self.velocity_x, max_speed))  # Limit horizontal speed by: max(absolute minimum, actual speed capped at maximum)-> restricted velocity
        print(self.velocity_x, end=' ', flush=True)
        x, y = self.position
        future_x = x + self.velocity_x

        # Check for screen boundaries
        if future_x < (0 + self.width / 2):
            future_x = (0 + self.width / 2)
        elif future_x > (WIDTH - (self.width / 2)):
            future_x = (WIDTH - (self.width / 2))
        
        self.position = (future_x, y)

        if acceleration_x == 0:
            if self.velocity_x > 0:
                self.velocity_x -= DECELERATION
            elif self.velocity_x < 0:
                self.velocity_x += DECELERATION
        
        
        

    def updateGravity(self):
        # Apply gravity
        self.velocity_y += GRAVITY
        x, y = self.position
        y += self.velocity_y

        # Check for ground collision
        if y >= GROUND_HEIGHT:
            y = GROUND_HEIGHT
            self.velocity_y = 0  # Reset vertical velocity on ground contact
        
        self.position = (x, y)

    
    def checkCollision(self, platform):
        selfRect = self.getRect()
        platformRect = platform.getRect()
        py.rect.colliderect()

    def getRect(self):
        x, y = self.position
        return py.Rect(x - (self.width / 2), y - (self.height / 2), self.width, self.height)

    def draw(self):
        x, y = self.position
        py.draw.rect(screen, GREEN, ((x - (self.width/2)), (y - (self.height/2)), self.width, self.height))
    
mainCharacter = Player("Player1")
mainCharacter.draw()

ground = py.Rect(0, GROUND_HEIGHT+25, WIDTH, 50)
rooms = {
    "Beginning": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
}

platforms = [
    py.Rect(0, GROUND_HEIGHT+25, WIDTH, 50)
]



class Room():
    def __init__(self, layout):
        self.layout = layout
        self.width = WIDTH
        self.height = HEIGHT
    
    def updateLayout():
        pass


running = True
while running:

    # Prepare the screen for next frame
    screen.fill((0, 0, 0))  # Clear the screen
    clock.tick(60) # Limit the frame rate to 60 FPS

    # Draw the environment/room -- TEMPORARY
    


    # Respond to player input
    for event in py.event.get():
        # Quit the game
        if event.type == py.QUIT:
            running = False
    
    keys = py.key.get_pressed()
    if keys[py.K_a] or keys[py.K_d]:
        if keys[py.K_a]:
            mainCharacter.movePlayer(-ACCELERATION)  # Move left
        if keys[py.K_d]:
            mainCharacter.movePlayer(ACCELERATION)
    else:
        mainCharacter.movePlayer(0)  # Stop horizontal movement if no input

    for platform in platforms:
        py.draw.rect(screen, (100, 100, 100), ground)



    mainCharacter.updateGravity()
    mainCharacter.draw()

    
    py.display.update()


py.quit()
