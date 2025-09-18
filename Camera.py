import pygame as py
from ColourPalettes import themeColourPalettes
WIDTH, HEIGHT = 1100, 800

class Camera:
    def __init__(self, zoom=1.4):
        self.x = 0
        self.y = 0
        self.xTarget = 0
        self.yTarget = 0
        self.smoothing = 0.6  # Lower = smoother, higher = more responsive
        self.zoom = zoom
        
        # Calculate effective screen size
        self.viewWidth = WIDTH / self.zoom
        self.viewHeight = HEIGHT / self.zoom
    
    def follow(self, room, xTarget, yTarget):
        # Calculate where the camera should be to center the target (accounting for zoom)
        self.xTarget = xTarget - self.viewWidth // 2
        self.yTarget = yTarget - self.viewHeight // 2
        
        # Smooth camera movement
        self.x += (self.xTarget - self.x) * self.smoothing
        self.y += (self.yTarget - self.y) * self.smoothing
        
        # Constrain camera to room bounds (accounting for zoom)
        roomWidth = room.columns * 50
        roomHeight = room.rows * 50
        
        self.x = max(0, min(self.x, roomWidth - self.viewWidth))
        self.y = max(0, min(self.y, roomHeight - self.viewHeight))
    
    def apply(self, x, y):
        """Convert world coordinates to screen coordinates with zoom"""
        xScreen = (x - self.x) * self.zoom
        yScreen = (y - self.y) * self.zoom
        return int(xScreen), int(yScreen)
    
    def applyRect(self, rect):
        """Apply camera offset and zoom to a rectangle"""
        xScreen = (rect.x - self.x) * self.zoom
        yScreen = (rect.y - self.y) * self.zoom
        screenWidth = rect.width * self.zoom
        screenHeight = rect.height * self.zoom
        return py.Rect(xScreen, yScreen, screenWidth, screenHeight)

                    
    def draw(self, camera):
        # Draw background
        backgroundColour = themeColourPalettes[self.theme]["background"]
        screen = py.display.get_surface()
        screen.fill(backgroundColour)
        
        # Draw platforms with camera offset
        for platform in self.platforms:
            platform.draw(camera)
        for object in self.interactives:
            object.draw(camera)