import pygame

def load_image(filename):
    #print(pygame.image.load(filename))
    return pygame.image.load(filename).convert_alpha()