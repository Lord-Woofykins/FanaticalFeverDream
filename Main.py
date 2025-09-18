# Import modules
import pygame as py

# Import classes from other files
from Player import Player
from Room import Room
from Camera import Camera
from uiManager import uiManager
from CollisionManager import CollisionManager
from GameManager import GameManager

py.init() # Initialize Pygame Modules

"""Setting Up Window"""
WIDTH, HEIGHT = 1100, 800

py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Roguelike Shapeshifter")
py.mouse.set_visible(False)

screen = py.display.get_surface()
clock = py.time.Clock()

# Create game objects
mainCharacter = Player()
camera = Camera()

# Create managers
uiManager = uiManager()
collisionManager = CollisionManager()
gameManager = GameManager(mainCharacter, 60)

# Initialize the first room
gameManager.currentRoom = Room()
gameManager.currentRoom.loadRoom() # load room from game manager

room = gameManager.currentRoom

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
    collisionManager.handleInteractions(mainCharacter, room, gameManager, camera)
    
    # Update camera to follow player
    camera.follow(room, mainCharacter.position[0], mainCharacter.position[1])
    print(f"Camera Position: ({camera.x:.2f}, {camera.y:.2f})")
    print(f"Player Position: ({mainCharacter.position[0]:.2f}, {mainCharacter.position[1]:.2f})")
    
    # Draw game for player
    room.draw(camera, screen)
    mainCharacter.draw(camera)
    uiManager.drawHealthBar(screen, 10, 10, 100, 40, mainCharacter.health, mainCharacter.maxHealth)

    # Update and draw enemies
    for enemy in room.enemies:
        enemy.patrol()
        enemy.draw(camera)
        collisionManager.checkEnemyCollisions(mainCharacter, room.enemies)

    # Update the display
    py.display.flip()
    clock.tick(gameManager.frametime)

py.quit()