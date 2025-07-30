import pygame as py

py.init() # Initialize Pygame Modules

# Setting Up Window
WIDTH, HEIGHT = 800, 600
nameOfGame = "Roguelike Shapeshifter TEST"

py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption(nameOfGame)

py.draw.rect(py.display.get_surface(), (100, 100, 100), (0, 550, 800, 50))




startingPosition = (400, 300)

class Player:
    def __init__(self, name):
        self.name = name
        self.position = startingPosition

    def move(self, x, y):
        self.position = (x, y)

Player("Player1")

class Room():
    def __init__(self, layout):
        self.layout = layout


running = True
while running:

    # Respond to player input
    for event in py.event.get():
        # Quit the game
        if event.type == py.QUIT:
            running = False

    py.display.update()


py.quit()