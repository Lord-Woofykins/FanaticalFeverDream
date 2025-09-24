import pygame as py
import sys
from Room import Room
WIDTH, HEIGHT = 1100, 800

class GameManager:
    def __init__(self, player, frametime, camera):
        self.currentRoom = None
        self.player = player
        self.camera = camera
        self.frametime = frametime
        
    def changeRoom(self, futureRoom, playerX, playerY, camera):
        """Change to a new room and position the player"""
        print(f"Changing to room: {futureRoom}")
        print(f"Spawning player at: ({playerX}, {playerY})")
        
        # Create and load the new room
        self.currentRoom = Room()
        self.currentRoom.loadRoom()
        
        # Position the player at the spawn point
        self.player.position[0] = playerX
        self.player.position[1] = playerY
        
        # Reset player physics
        self.player.xVelocity = 0
        self.player.yVelocity = 0

        camera.follow(self.currentRoom, playerX, playerY)

        self.transitionFade(camera)

    def transitionFade(self, camera):
        fadeSurface = py.Surface((WIDTH, HEIGHT), py.SRCALPHA)
        fadeSteps = 20  # increasing this value decreases fade speed
        screen = py.display.get_surface()
        clock = py.time.Clock()

        # Fade out
        for step in range(fadeSteps + 1):
            alpha = int((step / fadeSteps) * 255)

            # create a sudo game loop while fade occurs ro process essential changes
            self.currentRoom.draw(camera, screen)
            self.player.draw(camera)
            # overlay with alpha
            fadeSurface.fill((0, 0, 0, alpha))
            screen.blit(fadeSurface, (0, 0))
            py.display.flip()

            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
            clock.tick(self.frametime)

        # Fade in
        for i in range(fadeSteps + 1):
            alpha = int(((fadeSteps - i) / fadeSteps) * 255)
            self.currentRoom.draw(camera, screen)
            self.player.draw(camera)
            fadeSurface.fill((0, 0, 0, alpha))
            screen.blit(fadeSurface, (0, 0))
            py.display.flip()

            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
            clock.tick(self.frametime)
    
    def restart(self):
        pass