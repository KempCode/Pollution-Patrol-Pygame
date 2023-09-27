import gamescreen
import pygame
import util
from pygame.locals import *
from textwrap import fill
import sys

class EndScreen:
    # This is called when the screen is initialised
    def __init__(self, screen_manager, gamescreen):
        print('hello')
        self.manager = screen_manager

        background = util.load_image("start_background.jpeg")
        # background.fill((54, 34, 234))
        self.manager.screen_surface.blit(background, (0,0))

        #Renders the
        screen_width = self.manager.screen_surface.get_rect().width
        screen_height = self.manager.screen_surface.get_rect().height
        self.font = pygame.font.SysFont('comicsansms', screen_width // 16)
        textsurface = self.font.render('Game Over: Year {}'.format(gamescreen.facts.year), False, (0, 0, 0))
        half_text_width = textsurface.get_rect().width
        self.manager.screen_surface.blit(textsurface,(screen_width /2 - half_text_width /2, 30))

        self.font = pygame.font.SysFont('comicsansms', screen_width // 20)
        text2 = self.font.render('Fact about climate change:', True, (0, 0, 0))
        text2_width = text2.get_rect().width
        self.manager.screen_surface.blit(text2, (screen_width /2 - text2_width/2, 125))

        #Text that gives facts about sea level rising
        self.explanation_text = util.load_image("end_text.png")
        text_rect = self.explanation_text.get_rect()
        text_rect.topleft = (0, 200)
        self.manager.screen_surface.blit(self.explanation_text, text_rect)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
