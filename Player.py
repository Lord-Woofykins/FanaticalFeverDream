import pygame as py
startingPosition = [100, 800]
GRAVITY = 0.5
GREEN = (0, 128, 0)


class Player:
    def __init__(self, camera, width=40, height=70):
        self.camera = camera

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
        self.direction = 1

        self.jumpforce = 10.5
        self.onGround = False

        # Times in milliseconds
        self.attackCooldown = 500
        self.lastAttackTime = 0
        self.attackDisplayTime = 100
        self.isAttacking = False

        self.attackDamage = 20
        self.attackRange = 50

        self.maxHealth = 100
        self.health = self.maxHealth

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

    def attack(self, collisionManagerCallback):
        if self.checkAttackCooldown() == False:
            self.lastAttackTime = py.time.get_ticks()
            self.isAttacking = True
            collisionManagerCallback(self.getAttackRect())

    def updateGravity(self):
        self.yVelocity += GRAVITY

    def getRect(self):
        # Finding the top left corner from centre position
        return py.Rect(self.position[0] - self.width/2, self.position[1] - self.height/2, self.width, self.height)
    
    def getAttackRect(self):
        attackHeight = self.height // 2
        attackOffset = self.width // 2
        return py.Rect(
            self.position[0] + attackOffset * self.direction - (self.attackRange if self.direction == -1 else 0),
            self.position[1] - attackHeight,
            self.attackRange,
            self.height
        )

    def draw(self, camera):
        # Create a rect for the player in world coordinates
        playerRect = self.getRect()
        # Apply camera offset and zoom to the entire rectangle
        screenRect = camera.applyRect(playerRect)
        screen = py.display.get_surface()
        py.draw.rect(screen, GREEN, screenRect)
        # Draw attack rect if attacking
        if self.isAttacking:
            currentTime = py.time.get_ticks()
            if currentTime - self.lastAttackTime < self.attackDisplayTime:
                # Draw attack rect to visualise attack
                attackRect = self.getAttackRect()
                screenRect = camera.applyRect(attackRect)
                py.draw.rect(screen, (255, 0, 0), screenRect, 2)
            else:
                self.isAttacking = False

    def loseHealth(self, damage, gameManager):
        self.health -= damage
        if self.health <= 0:
            gameManager.restart()
    
    def checkAttackCooldown(self):
        # Compare current time to last attack time
        currentTime = py.time.get_ticks()
        if currentTime - self.lastAttackTime > self.attackCooldown:
            self.lastAttackTime = py.time.get_ticks()
            return False
        else:
            return True
    
    def reset(self):
        self.position = startingPosition.copy()
        self.health = self.maxHealth
        self.yVelocity = 0
        self.xVelocity = 0
        self.onGround = False
        self.stand()