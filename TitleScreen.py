import pygame as py
import sys
from ColourPalettes import themeColourPalettes

class TitleScreen:
    def __init__(self):
        self.antialiasing = False

        # Store a local reference to colours for easy access
        self.white = themeColourPalettes["CorePalette"]["white"]
        self.black = themeColourPalettes["CorePalette"]["black"]

        # Create fonts and reder text surfaces
        self.titleFont = py.font.Font("Jacquard12-Regular.ttf", 96)
        self.bodyFont = py.font.Font("Jacquard12-Regular.ttf", 64)
        self.titleText = self.titleFont.render("Roguelike Shapeshifter", self.antialiasing, self.white)
        self.startText = self.bodyFont.render("Press Enter to Select", self.antialiasing, self.white)
        self.newGameText = self.bodyFont.render("New Game", self.antialiasing, self.white)
        self.continueText = self.bodyFont.render("Continue", self.antialiasing, self.white)
        self.selectArrow = self.bodyFont.render(">>", self.antialiasing, self.white)

        # Allocate positions for text elements
        windowWidth, windowHeight = py.display.get_window_size()
        self.textRectCoords = {
            "titleText": (windowWidth // 2, windowHeight // 5),
            "startText": (windowWidth // 2, windowHeight // 3),
            "newGameText": (windowWidth // 2, windowHeight // 1.8),
            "continueText": (windowWidth // 2, int(windowHeight // 1.5)),
            "selectArrow": (windowWidth // 2 - 200, int(windowHeight // 1.8))
        }

        # Map text elements to surfaces
        self.textSurfaces = {
            "titleText": self.titleText,
            "startText": self.startText,
            "newGameText": self.newGameText,
            "continueText": self.continueText,
            "selectArrow": self.selectArrow
        }

        self.selectedOption = 0 # 0 for new game, 1 for continue

        self.clock = py.time.Clock()

    def display(self):
        screen = py.display.get_surface()
        screen.fill(self.black)

        for element in self.textRectCoords:
            elementX, elementY = self.textRectCoords[element]
            surface = self.textSurfaces[element]
            elementRect = surface.get_rect(center=(elementX, elementY))
            screen.blit(surface, elementRect)
        
        py.display.flip()

    def run(self):
        running = True
        while running:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        py.quit()
                        sys.exit()
                    if event.key == py.K_RETURN:
                        running = False
            self.display()
            self.clock.tick(60)