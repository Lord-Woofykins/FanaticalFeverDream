import pygame as py
import sys
from ColourPalettes import themeColourPalettes
from saveFile import saveGame
WIDTH, HEIGHT = 1100, 800

class TitleScreen:
    def __init__(self):
        self.antialiasing = False

        # Store a local reference to colours for easy access
        self.white = themeColourPalettes["CorePalette"]["white"]
        self.black = themeColourPalettes["CorePalette"]["black"]

        # Create fonts and reder text surfaces
        self.titleFont = py.font.Font("Jacquard12-Regular.ttf", 96)
        self.bodyFont = py.font.Font("Jacquard12-Regular.ttf", 64)
        self.titleText = self.titleFont.render("Fanatical Fever Dream", self.antialiasing, self.white)
        self.startText = self.bodyFont.render("Press Enter to Select", self.antialiasing, self.white)
        self.newGameText = self.bodyFont.render("New Game", self.antialiasing, self.white)
        self.continueText = self.bodyFont.render("Continue", self.antialiasing, self.white)
        self.keybindOptionText = self.bodyFont.render("Change Keybinds", self.antialiasing, self.white)
        self.selectArrow = self.bodyFont.render(">>", self.antialiasing, self.white)

        # Allocate positions for text elements
        windowWidth, windowHeight = py.display.get_window_size()
        self.textRectCoords = {
            "titleText": (windowWidth // 2, windowHeight // 5),
            "startText": (windowWidth // 2, windowHeight // 3),
            "newGameText": (windowWidth // 2, windowHeight // 1.8),
            "continueText": (windowWidth // 2, int(windowHeight // 1.5)),
            "keybindOptionText": (windowWidth // 2, int(windowHeight // 1.3)),
            "selectArrow": (windowWidth // 2 - 200, int(windowHeight // 1.8))
        }

        # Map text elements to surfaces
        self.textSurfaces = {
            "titleText": self.titleText,
            "startText": self.startText,
            "newGameText": self.newGameText,
            "continueText": self.continueText,
            "keybindOptionText": self.keybindOptionText,
            "selectArrow": self.selectArrow
        }

        self.selectedOption = 0 # 0 for new game, 1 for continue, etc.

        self.clock = py.time.Clock()

    def display(self):
        screen = py.display.get_surface()
        screen.fill(self.black)

        # Find text arrow coordinates based on selected option
        arrowOptions = ["newGameText", "continueText", "keybindOptionText"]
        selectedOption = arrowOptions[self.selectedOption]
        selectedX, selectedY = self.textRectCoords[selectedOption]
        self.textRectCoords["selectArrow"] = (selectedX - 250, selectedY)

        # Draw title screen elements
        for element in self.textRectCoords:
            elementX, elementY = self.textRectCoords[element]
            surface = self.textSurfaces[element]
            elementRect = surface.get_rect(center=(elementX, elementY))
            screen.blit(surface, elementRect)
        
        py.display.flip()

    def run(self, restartGameCallback, loadSaveCallback, loadGameDataCallback, keybinds):
        running = True
        while running:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        py.quit()
                        sys.exit()
                    if event.key == py.K_RETURN:
                        if self.selectedOption == 0:                            
                            restartGameCallback()
                        elif self.selectedOption == 1:
                            loadedData = loadGameDataCallback()
                            saveGame["playerHealth"] = loadedData["playerHealth"]
                            saveGame["playerScore"] = loadedData["playerScore"]
                            saveGame["playerPosition"] = loadedData["playerPosition"]
                            saveGame["dungeonMap"] =  loadedData["dungeonMap"]
                            saveGame["currentRoom"] =  loadedData["currentRoom"]
                            saveGame["playerPath"] = loadedData["playerPath"]
                            loadSaveCallback()
                        running = False
                        if self.selectedOption == 2:  # Change Keybinds
                            for action in keybinds:
                                self.changeKeybind(action, keybinds)
                    if event.key == py.K_UP or event.key == py.K_w:
                        self.selectedOption = max(0, self.selectedOption - 1)
                    elif event.key == py.K_DOWN or event.key == py.K_s:
                        self.selectedOption = min(2, self.selectedOption + 1)
            self.display()
            self.clock.tick(60)

    def changeKeybind(self, action, keybinds):
        """Waits for a key press and updates the keybind for the given action"""
        waiting = True
        screen = py.display.get_surface()
        font = self.bodyFont
        prompt = font.render(f"Press a key for {action}", True, self.white)
        rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        while waiting:
            screen.fill(self.black)
            screen.blit(prompt, rect)
            py.display.flip()
            
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
                if event.type == py.KEYDOWN:
                    keybinds[action] = event.key
                    waiting = False