import gamescreen
import pygame
import util
from pygame.locals import *
from textwrap import fill
import sys

class MenuScreen:
    # This is called when the screen is initialised
    def __init__(self, screen_manager):
        self.manager = screen_manager

        self.background = util.load_image("start_background.jpeg")
        self.background = pygame.transform.scale(self.background, self.manager.screen_surface.get_rect().size)
        self.manager.screen_surface.blit(self.background, (0,0))





        #Renders the
        screen_width = self.manager.screen_surface.get_rect().width
        screen_height = self.manager.screen_surface.get_rect().height
        self.font = pygame.font.SysFont('comicsansms', screen_width // 8)
        textsurface = self.font.render('Pollution Patrol', True, (0, 0, 0))
        half_text_width = textsurface.get_rect().width
        self.manager.screen_surface.blit(textsurface,(screen_width /2 - half_text_width /2, 30))

        self.font = pygame.font.SysFont('comicsansms', screen_width // 20)
        text2 = self.font.render('Global warming is not fake news.', True, (0, 0, 0))
        text2_width = text2.get_rect().width
        self.manager.screen_surface.blit(text2, (screen_width /2 - text2_width/2, 160))

        #Text that explains the game.
        self.explanation_text = util.load_image("explanation_text.png")
        text_rect = self.explanation_text.get_rect()
        text_rect.topleft = (0, 175)
        self.manager.screen_surface.blit(self.explanation_text, text_rect)


        self.button_image = util.load_image("start_button.png")
        imagerect = self.button_image.get_rect()
        image_width = imagerect.width
        imagerect.topleft = (screen_width /2 - image_width /2, screen_height // 1.6)
        self.manager.screen_surface.blit(self.button_image,imagerect)
        pygame.display.flip()




    # This code is called in a loop
    def update(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            # print("hello")
            newScreen = gamescreen.GameScreen(self.manager)
            self.manager.set_screen(newScreen)
