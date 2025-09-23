import pygame as py
from ColourPalettes import themeColourPalettes

class uiManager:
    def __init__(self):
        try:
            self.scoreFont = py.font.Font("Jacquard12-Regular.ttf", 48)
        except FileNotFoundError:
            self.scoreFont = py.font.Font(None, 48)  # Use default font

    def drawHealthBar(self, surface, x, y, width, height, currentHealth, maxHealth):
        # Calculate a ratio for the health status
        healthRatio = currentHealth / maxHealth
        py.draw.rect(surface, themeColourPalettes["UI"]["background"], (x, y, width, height)) # Background
        py.draw.rect(surface, themeColourPalettes["UI"]["foreground"], (x, y, int(width * healthRatio), height)) # Health bar
        py.draw.rect(surface, themeColourPalettes["UI"]["border"], (x, y, width, height), 2) # Border
    
    def drawScoreTracker(self, surface, x, y, width, height, currentScore):
        # Create font and text
        self.scoreText = self.scoreFont.render(str(currentScore), False, themeColourPalettes["UI"]["scoreColour"])
        
        # Draw the background rectangle
        py.draw.rect(surface, themeColourPalettes["UI"]["background"], (x, y, width, height))
        
        # Calculate position to center the text in the rectangle
        textRect = self.scoreText.get_rect()
        textX = x + (width - textRect.width) // 2
        textY = y + (height - textRect.height) // 2
        
        # Draw the text on the surface
        surface.blit(self.scoreText, (textX, textY))
