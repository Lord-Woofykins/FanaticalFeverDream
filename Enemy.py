import pygame as py

class Enemy:
    def __init__(self, xPosition, yPosition, width, height, speed, direction, patrolRange):
        self.position = [xPosition, yPosition]
        self.width = width
        self.height = height
        self.speed = speed
        self.direction = direction # 1 is right, -1 is left
        self.patrolRange = patrolRange

    
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
        enemyRect = py.Rect(self.position[0] - camera[0], self.position[1] - camera[1], self.width, self.height)
        py.draw.rect(py.display.get_surface(), self.colour, enemyRect)  # Draw enemy as a red rectangle