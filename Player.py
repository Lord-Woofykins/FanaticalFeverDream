import pygame as py
import os
startingPosition = [550, 550]
GRAVITY = 0.5


class Player:
    def __init__(self, camera, width=40, height=64):
        self.camera = camera

        self.position = startingPosition.copy()
        self.width = width
        self.height = height

        self.standHeight = height
        self.crouchHeight = min(50, height/2) # Dynamic height adjustment for changing later
        self.isCrouching = False  # Track crouching state

        self.maxSpeed = 8
        self.standSpeed = 8
        self.crouchSpeed = 3

        self.yVelocity = 0
        self.xVelocity = 0
        self.acceleration = 1
        self.deceleration = 2
        self.direction = 1

        self.jumpForce = 10.5
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

        self.spriteAnimations = {}
        spriteFolders = ["Attack_1", "Attack_2", "Charge", "Crouch", "Dead", "Fireball", "Flamejet", "Hurt", "Idle", "Jump", "Run", "Walk"]
        basePath = os.path.join(os.path.dirname(__file__), "Fire Wizard")

        for spriteType in spriteFolders:
            # Find the path to the spriteFolder/Type
            folderPath = os.path.join(basePath, spriteType)
            frames = []

            # Assign each sprite as a frame (sorted to ensure they are in order)
            if os.path.exists(folderPath):
                for filename in sorted(os.listdir(folderPath)):
                    framePath = os.path.join(folderPath, filename)
                    if os.path.isfile(framePath) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                        frame = py.image.load(framePath).convert_alpha()
                        frames.append(frame)

            self.spriteAnimations[spriteType] = frames

        self.animationMap = {
            "idle": "Idle",
            "run": "Run",
            "walk": "Walk",
            "crouch": "Crouch",
            "jump": "Jump",
            "attack": "Attack_1",
            "hurt": "Hurt",
            "dead": "Dead",
            "fire": "Fireball"
        }
        
        # Define which animations should not loop
        self.nonLoopingAnimations = {"attack", "hurt", "dead", "fire", "jump"}
        
        self.animationStatus = "idle"
        self.animationKey = self.animationMap.get(self.animationStatus)
        self.frameIndex = 0
        self.frameDuration = 100
        self.previousFrameTime = 0
        self.loopAnimation = True

        self.currentScore = 0

    def movePlayer(self, xAcceleration):
        self.xVelocity += xAcceleration
        self.xVelocity = max(-self.maxSpeed, min(self.xVelocity, self.maxSpeed))  # Clamp speed

        # Set direction based on movement
        if xAcceleration > 0:
            self.direction = 1
        elif xAcceleration < 0:
            self.direction = -1

        # Apply deceleration when no input is given (regardless of ground state)
        if xAcceleration == 0:
            if self.xVelocity > 0:
                self.xVelocity = max(0, self.xVelocity - self.deceleration)
            elif self.xVelocity < 0:
                self.xVelocity = min(0, self.xVelocity + self.deceleration)

            if abs(self.xVelocity) < 0.1:
                self.xVelocity = 0

        # Handle animation based on current state priorities
        if self.isCrouching:
            if xAcceleration != 0:
                # Allow crawling while crouched
                self.setAnimation("crouch")
            else:
                self.setAnimation("crouch")  # Stay crouched even when idle
        elif not self.onGround:
            self.setAnimation("jump")
        elif xAcceleration != 0:
            self.setAnimation("run")
        else:
            if self.onGround:
                self.setAnimation("idle")

    def crouch(self):
        if not self.isCrouching:  # Only crouch if not already crouching
            self.height = self.crouchHeight
            self.position[1] += (self.standHeight - self.crouchHeight) / 2 # Adjusting position to stay grounded
            self.maxSpeed = self.crouchSpeed
            self.isCrouching = True
        self.setAnimation("crouch")  # Always set crouch animation when crouch is called
        
    def stand(self):
        if self.isCrouching:  # Only stand if currently crouching
            self.height = self.standHeight
            self.position[1] -= (self.standHeight - self.crouchHeight) / 2 # Adjusting position to normal height
            self.maxSpeed = self.standSpeed
            self.isCrouching = False
        
    def jump(self):
        if self.onGround:  # Only jump if on ground
            self.yVelocity = -self.jumpForce
            self.setAnimation("jump")

    def attack(self, collisionManagerCallback, room):
        if self.checkAttackCooldown() == False:
            self.lastAttackTime = py.time.get_ticks()
            self.isAttacking = True
            collisionManagerCallback(self.getAttackRect(), room, self.increaseScore)
            self.setAnimation("attack")
    
    def increaseScore(self):
        self.currentScore += 1

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
    
    def setAnimation(self, status):
        # Don't change animation if we're in a higher priority non-looping animation that hasn't finished
        if not self.loopAnimation and self.animationStatus in self.nonLoopingAnimations:
            frames = self.spriteAnimations.get(self.animationKey)
            if frames and self.frameIndex < len(frames) - 1:
                # Animation is still playing, don't change it unless it's the same type or higher priority
                if status not in ["dead", "hurt"]:  # Only death and hurt can interrupt other non-looping animations
                    return

        futureKey = self.animationMap.get(status)
        if futureKey != self.animationKey:
            self.animationKey = futureKey
            # Reset frame values for new animation
            self.frameIndex = 0
            self.previousFrameTime = py.time.get_ticks()
            self.animationStatus = status
            # Set loop status based on animation type
            self.loopAnimation = status not in self.nonLoopingAnimations

    def updateAnimation(self):
        frames = self.spriteAnimations.get(self.animationKey)
        if not frames:
            print("An error occurred retrieving animation")
            return
        
        # Determining whether enough time has passed for another frame
        currentTime = py.time.get_ticks()
        if currentTime - self.previousFrameTime >= self.frameDuration:
            self.previousFrameTime = currentTime
            self.frameIndex += 1
            # Determine whether this animation should be looped
            if self.frameIndex >= len(frames):
                if self.loopAnimation:
                    self.frameIndex = 0 # Restart animation
                else:
                    self.frameIndex = len(frames) - 1 # Keeping animation on final frame

    def draw(self, camera):
        # Create a rect for the player in world coordinates
        playerRect = self.getRect()
        # Apply camera offset and zoom to the entire rectangle
        screenRect = camera.applyRect(playerRect)
        screen = py.display.get_surface()

        # Hitbox code for testing
        # py.draw.rect(screen, (0, 0, 0), screenRect)
        

        # Draw sprite on top of the rectangle
        frames = self.spriteAnimations.get(self.animationKey)
        if frames:
            frame = frames[self.frameIndex]
            
            # Scale sprite maintaining its natural aspect ratio
            originalWidth = frame.get_width()
            originalHeight = frame.get_height()
            
            # Use standHeight for sprite scaling to keep consistent size when crouching
            spriteHeight = self.standHeight if self.isCrouching else self.height
            scaleRatio = (spriteHeight * 3) / originalHeight
            scaledWidth = int(originalWidth * scaleRatio)
            scaledHeight = int(originalHeight * scaleRatio)
            
            frameSurface = py.transform.scale(frame, (scaledWidth, scaledHeight))
            
            if self.direction == -1:
                frameSurface = py.transform.flip(frameSurface, True, False)
            
            # Position sprite: center horizontally, align bottom with player rect
            spriteX = screenRect.centerx - scaledWidth // 2
            spriteY = screenRect.bottom - scaledHeight
            
            screen.blit(frameSurface, (spriteX, spriteY))

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
            self.setAnimation("dead")
            
    
    def checkAttackCooldown(self):
        # Compare current time to last attack time
        currentTime = py.time.get_ticks()
        if currentTime - self.lastAttackTime > self.attackCooldown:
            self.lastAttackTime = py.time.get_ticks()
            return False
        else:
            return True
    
    def reset(self):
        self.position = [0, 0]
        self.health = self.maxHealth
        self.height = 64
        self.yVelocity = 0
        self.xVelocity = 0
        self.onGround = False
        self.isCrouching = False
        self.stand()