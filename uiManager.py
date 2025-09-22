import pygame as py
from ColourPalettes import themeColourPalettes

class uiManager:
    def __init__(self):
        pass

    def drawHealthBar(self, surface, x, y, width, height, currentHealth, maxHealth):
        # Calculate a ratio for the health status
        healthRatio = currentHealth / maxHealth
        py.draw.rect(surface, themeColourPalettes["UI"]["healthBarBackground"], (x, y, width, height)) # Background
        py.draw.rect(surface, themeColourPalettes["UI"]["healthBarForeground"], (x, y, int(width * healthRatio), height)) # Health bar
        py.draw.rect(surface, themeColourPalettes["UI"]["healthBarBorder"], (x, y, width, height), 2) # Border
    
    def drawScoreTracker(self, surface, x, y, width, height, currentScore):
        py.draw.rect(surface, themeColourPalettes["CorePalette"]["black"], (x, y, width, height))
        self.scoreFont = py.font.Font("Jacquard12-Regular.ttf", 64)
        self.scoreText = self.scoreFont.render()
