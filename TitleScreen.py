import pygame as py
import sys
from ColourPalettes import themeColourPalettes

class TitleScreen:
    def __init__(self):
        self.white = themeColourPalettes["CorePalette"]["white"]
        self.black = themeColourPalettes["CorePalette"]["black"]

        self.font = py.font.Font("Jacquard12-Regular.ttf", 74)
        self.titleText = self.font.render("Roguelike Shapeshifter", True, self.white)
        self.startText = self.font.render("Press Enter to Start", True, self.white)

        self.clock = py.time.Clock()

    def display(self):
        screen = py.display.get_surface()
        screen.fill(self.black)

        windowWidth, windowHeight = py.display.get_window_size()
        titleRect = self.titleText.get_rect(center=(windowWidth // 2, windowHeight // 3))
        startRect = self.startText.get_rect(center=(windowWidth // 2, windowHeight * 2 // 3))
        screen.blit(self.titleText, titleRect)
        screen.blit(self.startText, startRect)
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