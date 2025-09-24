import pygame as py
class CollisionManager:
    def __init__(self, room):
        self.room = room

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
    
    def handleInteractions(self, player, room, gameManager, camera):
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
                transition.trigger(gameManager, camera)

    def checkEnemyCollisions(self, player, enemies, gameManager):
        playerRect = player.getRect()
        for enemy in enemies:
            if playerRect.colliderect(enemy.getRect()):
                player.loseHealth(enemy.damage, gameManager)
    
    def checkEnemyHits(self, attackRect):
        for enemy in self.room.enemies:
            if attackRect.colliderect(enemy.getRect()):
                pass