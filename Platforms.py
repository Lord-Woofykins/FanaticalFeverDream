import pygame as py
from ColourPalettes import themeColourPalettes

WIDTH, HEIGHT = 1100, 800

class Platform:
    def __init__(self, x, y, width, height, platformType, theme):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.platformType = platformType
        self.theme = theme
    
    def getRect(self):
        return py.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, camera):
        screen = py.display.get_surface()
        # Only draw if platform is visible on screen (with zoom consideration)
        screenRect = camera.applyRect(self.getRect())
        if (screenRect.right > -screenRect.width and screenRect.left < WIDTH + screenRect.width and 
            screenRect.bottom > -screenRect.height and screenRect.top < HEIGHT + screenRect.height):
            platformColour = themeColourPalettes[self.theme][self.platformType]
            py.draw.rect(screen, platformColour, screenRect)

class Door(Platform):
    def __init__(self, x, y, width, height, platformType, theme):
        super().__init__(x, y, width, height, platformType, theme)
        self.isOpen = False

    def trigger(self):
        self.isOpen = True
        self.platformType = "openDoor"

class Transition(Platform):
    def __init__(self, x, y, width, height, platformType, targetRoom, playerSpawnX, playerSpawnY, theme):
        super().__init__(x, y, width, height, platformType, theme)
        self.targetRoom = targetRoom
        self.playerSpawnX = playerSpawnX
        self.playerSpawnY = playerSpawnY

    def trigger(self, gameManager, camera):
        gameManager.changeRoom(self.targetRoom, self.playerSpawnX*50, self.playerSpawnY*50, camera)

class Key(Platform):
    def __init__(self, x, y, width, height, platformType, targetInteractive, theme):
        super().__init__(x, y, width, height, platformType, theme)
        self.triggered = False
        self.targetInteractive = targetInteractive

    def trigger(self):
        if not self.triggered:
            self.triggered = True
            self.targetInteractive.trigger()