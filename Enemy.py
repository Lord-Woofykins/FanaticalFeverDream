import pygame as py

class Enemy:
    def __init__(self, xPosition, yPosition, width, height, speed, direction, patrolRange):
        self.position = [xPosition, yPosition]
        self.width = width
        self.height = height
        self.speed = speed
        self.direction = direction # 1 is right, -1 is left
        self.patrolRange = patrolRange
    
    def getRect(self):
        return py.Rect(self.position[0], self.position[1] - (self.height-50), self.width, self.height)

    
class GroundEnemy(Enemy):
    def __init__(self, xPosition, yPosition, width, height, speed, direction, patrolRange, colour):
        super().__init__(xPosition, yPosition, width, height, speed, direction, patrolRange)
        self.xInitial = xPosition
        self.colour = colour

    def patrol(self):
        self.position[0] += self.speed * self.direction
        if abs(self.position[0] - self.xInitial) >= self.patrolRange:
            self.direction *= -1  # Change direction
    
    def draw(self, camera):
        enemyRect = self.getRect()
        screenRect = camera.applyRect(enemyRect)
        py.draw.rect(py.display.get_surface(), self.colour, screenRect)

class FlyingEnemy(Enemy):
    def __init__(self, xPosition, yPosition, width, height, speed, direction, patrolRange, colour):
        super().__init__(xPosition, yPosition, width, height, speed, direction, patrolRange)
        self.xInitial = xPosition
        self.colour = colour

    def patrol(self):
        self.position[0] += self.speed * self.direction
        if abs(self.position[0] - self.xInitial) >= self.patrolRange:
            self.direction *= -1  # Change direction
    
    def draw(self, camera):
        enemyRect = self.getRect()
        py.draw.rect(py.display.get_surface(), self.colour, enemyRect)

class DemonEnemy(Enemy):
    def __init__(self, xPosition, yPosition, width, height, speed, direction, patrolRange, colour):
        super().__init__(xPosition, yPosition, width, height, speed, direction, patrolRange)
        self.xInitial = xPosition
        self.colour = colour

    def patrol(self):
        self.position[0] += self.speed * self.direction
        if abs(self.position[0] - self.xInitial) >= self.patrolRange:
            self.direction *= -1  # Change direction
    
    def draw(self, camera):
        enemyRect = py.Rect(self.position[0], self.position[1] - (self.height-50), self.width, self.height)
        py.draw.rect(py.display.get_surface(), self.colour, enemyRect)