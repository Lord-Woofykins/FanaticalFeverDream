import pygame as py
import sys

# Import classes form other files
from Enemies import GroundEnemy, FlyingEnemy, DemonEnemy
from Player import Player
from Room import Room
from Camera import Camera

# Import dictionaries
from ColourPalettes import themeColourPalettes

py.init() # Initialize Pygame Modules

# Setting Up Window
WIDTH, HEIGHT = 1100, 800

FRAMETIME = 60

JUMPFORCE = 10.5    

nameOfGame = "Roguelike Shapeshifter"

py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption(nameOfGame)
screen = py.display.get_surface()

py.mouse.set_visible(False)

clock = py.time.Clock()


class GameManager:
    def __init__(self, player):
        self.currentRoom = None
        self.player = player
        
    def changeRoom(self, futureRoom, playerX, playerY):
        """Change to a new room and position the player"""
        print(f"Changing to room: {futureRoom}")
        print(f"Spawning player at: ({playerX}, {playerY})")
        
        # Create and load the new room
        self.currentRoom = Room(futureRoom)
        self.currentRoom.loadRoom()
        
        # Position the player at the spawn point
        self.player.position[0] = playerX
        self.player.position[1] = playerY
        
        # Reset player physics
        self.player.xVelocity = 0
        self.player.yVelocity = 0

        camera.follow(self.currentRoom, playerX, playerY)

        self.transitionFade()

    def transitionFade(self):
        fadeSurface = py.Surface((WIDTH, HEIGHT), py.SRCALPHA)
        fadeSteps = 20  # increasing this value decreases fade speed

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
            clock.tick(FRAMETIME)

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
            clock.tick(FRAMETIME)
        

class CollisionManager:
    def handleCollisions(self, player, room):
        # Apply vertical movement first
        player.position[1] += player.yVelocity
        playerRect = player.getRect()
        
        # Check for vertical collisions
        for platform in room.platforms:
            if platform.platformType == "openDoor" and platform.isOpen:
                continue
            platRect = platform.getRect()
            if playerRect.colliderect(platRect):
                if player.yVelocity > 0:  # Falling down - landed on platform
                    player.position[1] = platform.y - player.height / 2
                    player.yVelocity = 0
                elif player.yVelocity < 0:  # Moving up - hit ceiling
                    player.position[1] = platform.y + platform.height + player.height / 2
                    player.yVelocity = 0
                break

        # Apply horizontal movement
        player.position[0] += player.xVelocity
        playerRect = player.getRect()
        
        # Check horizontal collisions
        for platform in room.platforms:
            if platform.platformType == "openDoor" and platform.isOpen:
                continue
            platRect = platform.getRect()
            if playerRect.colliderect(platRect):
                if player.xVelocity > 0:  # Moving right
                    player.position[0] = platform.x - player.width / 2
                elif player.xVelocity < 0:  # Moving left
                    player.position[0] = platform.x + platform.width + player.width / 2
                player.xVelocity = 0
                break

        # Check if player is on ground (separate check after movement)
        player.onGround = False
        groundCheckRect = py.Rect(player.position[0] - player.width/2, player.position[1] + player.height/2, player.width, 2)  # Small rect below player
        
        for platform in room.platforms:
            if groundCheckRect.colliderect(platform.getRect()):
                player.onGround = True
                break
    
    def handleInteractions(self, player, room, gameManager):
        playerRect = player.getRect()

        # Handle regular interactives (keys, etc.)
        for object in room.interactives:
            objectRect = object.getRect()
            if playerRect.colliderect(objectRect):
                try:
                    object.trigger()
                except AttributeError:
                    print("Interactive Failed To Trigger")
                    continue

        # Handle room transitions
        for transition in room.transitions:
            transitionRect = transition.getRect()
            if playerRect.colliderect(transitionRect):
                try:
                    transition.trigger(gameManager)
                except:
                    print("Transition Failed To Trigger")
                    continue

    def checkEnemyCollisions(self, player, enemies):
        playerRect = player.getRect()
        for enemy in enemies:
            enemyRect = py.Rect(enemy.position[0] - enemy.width/2, enemy.position[1] - enemy.height/2, enemy.width, enemy.height)
            if playerRect.colliderect(enemyRect):
                pass



# Create game objects
mainCharacter = Player()
gameManager = GameManager(mainCharacter)
gameManager.currentRoom = Room()
gameManager.currentRoom.loadRoom() # load room from game manager

# For compatibility with existing code
room = gameManager.currentRoom

collisionManager = CollisionManager()
camera = Camera()

"""Main game loop"""
running = True
while running:
    # Keep the room reference to that in the game manager
    room = gameManager.currentRoom
    
    # Handle events
    for event in py.event.get():
        # Quit game
        if event.type == py.QUIT:
            running = False
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                running = False
        # Movement events
            if event.key == py.K_s:
                mainCharacter.crouch()
            if event.key == py.K_DOWN:
                mainCharacter.crouch()
            if event.key == py.K_w:
                mainCharacter.jump()
            if event.key == py.K_UP:
                mainCharacter.jump()
        if event.type == py.KEYUP:
            if event.key == py.K_s:
                mainCharacter.stand()
            if event.key == py.K_DOWN:
                mainCharacter.stand()
    
    # Handle continuous input
    keys = py.key.get_pressed()
    if keys[py.K_a] or keys[py.K_d]:
        if keys[py.K_a]:
            mainCharacter.movePlayer(-mainCharacter.acceleration)
        elif keys[py.K_d]:
            mainCharacter.movePlayer(mainCharacter.acceleration)
    elif keys[py.K_LEFT] or keys[py.K_RIGHT]:
        if keys[py.K_LEFT]:
            mainCharacter.movePlayer(-mainCharacter.acceleration)
        elif keys[py.K_RIGHT]:
            mainCharacter.movePlayer(mainCharacter.acceleration)
    else:
            mainCharacter.movePlayer(0)  # Stop horizontal movement if no input

    # Update physics
    mainCharacter.updateGravity()
    collisionManager.handleCollisions(mainCharacter, room)

    # Process interactions
    collisionManager.handleInteractions(mainCharacter, room, gameManager)
    
    # Update camera to follow player
    camera.follow(room, mainCharacter.position[0], mainCharacter.position[1])
    print(f"Camera Position: ({camera.x:.2f}, {camera.y:.2f})")
    print(f"Player Position: ({mainCharacter.position[0]:.2f}, {mainCharacter.position[1]:.2f})")
    
    # Draw game for player
    room.draw(camera, screen)
    mainCharacter.draw(camera)

    # Update and draw enemies
    for enemy in room.enemies:
        enemy.patrol()
        enemy.draw(camera)
        collisionManager.checkEnemyCollisions(mainCharacter, room.enemies)

    # Update the display
    py.display.flip()
    clock.tick(FRAMETIME)

py.quit()