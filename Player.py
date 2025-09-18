import pygame as py
startingPosition = [100, 800]
GRAVITY = 0.5
GREEN = (0, 128, 0)


class Player:
    def __init__(self, width=40, height=70):
        self.position = startingPosition.copy()
        self.width = width
        self.height = height

        self.standHeight = height
        self.crouchHeight = min(50, height/2) # Dynamic height adjustment for changing later

        self.maxSpeed = 8
        self.standSpeed = 8
        self.crouchSpeed = 3

        self.yVelocity = 0
        self.xVelocity = 0
        self.acceleration = 1
        self.deceleration = 2

        self.jumpforce = 10.5

        self.onGround = False

        self.health = 100

    def movePlayer(self, xAcceleration):
        self.xVelocity += xAcceleration
        self.xVelocity = max(-self.maxSpeed, min(self.xVelocity, self.maxSpeed)) # Limit horizontal speed by: max(absolute minimum, actual speed capped at maximum)-> restricted velocity

        if xAcceleration == 0:
            if self.xVelocity > 0:
                self.xVelocity = max(0, self.xVelocity - self.deceleration)
            elif self.xVelocity < 0:
                self.xVelocity = min(0, self.xVelocity + self.deceleration)
    
    def crouch(self):
        self.height = self.crouchHeight
        self.position[1] += self.height / 2 # Adjusting position to stay grounded
        self.maxSpeed = self.crouchSpeed
        
    def stand(self):
        self.height = self.standHeight
        self.position[1] -= self.crouchHeight / 2 # Adjusting position to normal height
        self.maxSpeed = self.standSpeed
        
    def jump(self):
        if self.onGround:  # Only jump if on ground
            self.yVelocity = -self.jumpforce

    def updateGravity(self):
        self.yVelocity += GRAVITY

    def getRect(self):
        return py.Rect(self.position[0] - self.width/2, self.position[1] - self.height/2, self.width, self.height)

    def draw(self, camera):
        # Create a rect for the player in world coordinates
        playerRect = self.getRect()
        # Apply camera offset and zoom to the entire rectangle
        screenRect = camera.applyRect(playerRect)
        screen = py.display.get_surface()
        py.draw.rect(screen, GREEN, screenRect)
    
    def loseHealth(self, damage):
        self.health -= damage
        if self.health <= 0:
            pass