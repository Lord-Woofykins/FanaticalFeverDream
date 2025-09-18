import pygame
from ColourPalettes import themeColourPalettes

class uiManager:
    def __init__(self):
        pass

    def drawHealthBar(self, surface, x, y, width, height, currentHealth, maxHealth):
        # Calculate a ratio for the health status
        healthRatio = currentHealth / maxHealth
        pygame.draw.rect(surface, themeColourPalettes["UI"]["healthBarBackground"], (x, y, width, height)) # Background
        pygame.draw.rect(surface, themeColourPalettes["UI"]["healthBarForeground"], (x, y, int(width * healthRatio), height)) # Health bar
        pygame.draw.rect(surface, themeColourPalettes["UI"]["healthBarBorder"], (x, y, width, height), 2) # Border