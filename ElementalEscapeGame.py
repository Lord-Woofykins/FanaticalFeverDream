import pygame as py

py.init() # Initialize Pygame Modules

# Constants
GREEN = (0, 128, 0)


# Setting Up Window
WIDTH, HEIGHT = 800, 600

GRAVITY = 0.5
GROUND_HEIGHT = 525

nameOfGame = "Roguelike Shapeshifter TEST"

py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption(nameOfGame)

clock = py.time.Clock()

startingPosition = (400, 300)

class Player:
    def __init__(self, name, width=50, height=50):
        self.name = name
        self.position = startingPosition
        self.width = width
        self.height = height

        self.velocity_y = 0




        print(f"Player {self.name} created at position {self.position}")

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

    def draw(self):
        x, y = self.position
        py.draw.rect(py.display.get_surface(), GREEN, ((x - (self.width/2)), (y - (self.height/2)), self.width, self.height))
    


mainCharacter = Player("Player1")
mainCharacter.draw()

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
    py.display.get_surface().fill((0, 0, 0))  # Clear the screen
    clock.tick(60) # Limit the frame rate to 60 FPS

    # Draw the environment/room -- TEMPORARY
    py.draw.rect(py.display.get_surface(), (100, 100, 100), (0, 550, 800, 50))



    # Respond to player input
    for event in py.event.get():
        # Quit the game
        if event.type == py.QUIT:
            running = False


    mainCharacter.updateGravity()
    mainCharacter.draw()

    
    py.display.update()


py.quit()
