import pygame
from pygame.locals import *

import menuscreen

SCREEN_RECT = Rect(0, 0, 800, 800)

class GameManager:
    current_screen = None
    screen_surface = None

    def main(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Henlo")
        self.screen_surface = pygame.display.set_mode(SCREEN_RECT.size)

        self.set_screen(menuscreen.MenuScreen(self))


        running = True
        while running:
            self.current_screen.update()

    def set_screen(self, new_screen):
        self.current_screen = new_screen

GameManager().main()
