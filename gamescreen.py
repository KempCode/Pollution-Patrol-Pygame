import pygame
from pygame.locals import *
import util
import sys
import random
import endscreen


class GameScreen:
    def __init__(self, screen_manager):
        self.manager = screen_manager

        self.background = util.load_image("nz.jpg")
        self.background = pygame.transform.scale(self.background, self.manager.screen_surface.get_rect().size)
        self.manager.screen_surface.blit(self.background, (0,0))
        pygame.display.flip()

        self.all_group = pygame.sprite.RenderUpdates()
        self.bullets_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.player = Player(self, self.all_group)
        self.water = Water(self, self.all_group)
        self.facts = FactsDisplay(self, self.all_group)

        self.clock = pygame.time.Clock()
        self.updateCount = 0
        self.shot_cooldown = 0

        # NOTE temporary:
        # self.water_rise(500)


    def update(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()

        self.all_group.clear(self.manager.screen_surface, self.background)
        self.all_group.update()

        pygame.sprite.groupcollide(self.bullets_group, self.enemy_group, True, True)

        if keys[K_LEFT]:
            # print("left")
            self.player.move(Player.LEFT)
        elif keys[K_RIGHT]:
            # print("right")
            self.player.move(Player.RIGHT)
        elif keys[K_SPACE] and self.shot_cooldown > 30:
            Bullet(self, (self.all_group, self.bullets_group), self.player.rect.midtop)
            self.shot_cooldown = 0
            #self.water_rise()

        if(self.updateCount % 60 == 0):
            # spawn enemy
            Enemy(self, (self.all_group, self.enemy_group))
        
        if(self.updateCount % 10 == 0):
            self.water_rise(1)
        
        dirty_areas = self.all_group.draw(self.manager.screen_surface)
        pygame.display.update(dirty_areas)

        # print(player.rect)

        self.clock.tick(60)
        self.updateCount += 1
        self.shot_cooldown += 1

    def water_rise(self, amount):
        self.water.rise(-amount)
        self.player.rect.move_ip(0, -amount)



class Player(pygame.sprite.Sprite):
    #direction types
    LEFT = 0
    RIGHT = 1


    def __init__(self, game_screen, containers):
        self.game_screen = game_screen

        pygame.sprite.Sprite.__init__(self, containers)
        self.image = util.load_image("player.png")

        self.rect = self.image.get_rect(midbottom = game_screen.manager.screen_surface.get_rect().midbottom)


    def move(self, direction):
        self.rect.move_ip(-10 if direction == self.LEFT else 10, 0)
        self.rect.clamp_ip(self.game_screen.manager.screen_surface.get_rect())

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game_screen, containers, position):
        self.game_screen = game_screen

        pygame.sprite.Sprite.__init__(self, containers)
        self.image = util.load_image("bullet.png")

        self.rect = self.image.get_rect(midbottom = position)

    def update(self):
        self.rect.move_ip(0, -10)
        if self.rect.top < 0:
            self.kill()

class Water(pygame.sprite.Sprite):

    def __init__(self, game_screen, containers):
        pygame.sprite.Sprite.__init__(self, containers)
        self.game_screen = game_screen
        self.image = util.load_image("water2.png")

        self.y = game_screen.manager.screen_surface.get_rect().bottom
        self.rect = self.image.get_rect(top = self.y - 30)
    
    def update(self):
        pass

    def rise(self, amount):
        self.y += amount
        self.rect.move_ip(0, amount)
        if self.y < 200:
            self.game_screen.enemy_group.empty()
            self.game_screen.bullets_group.empty()
            self.game_screen.all_group.empty()
            self.game_screen.manager.set_screen(endscreen.EndScreen(self.game_screen.manager, self.game_screen))
    
    # from 0 to 1
    # NOTE not used
    def set_level(self, level):
        self.rect.top = level * -self.game_screen.manager.screen_surface.get_rect().height
        if level >= 1:
            pass
            # goto end screen

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game_screen, containers):
        pygame.sprite.Sprite.__init__(self, containers)
        if bool(random.getrandbits(1)):
            self.image = util.load_image("rubbish.png")
        else:
            self.image = util.load_image("rub2.png")

        self.game_screen = game_screen
        x = random.randint(50, self.game_screen.manager.screen_surface.get_rect().width - 50)
        # print(x)
        self.rect = self.image.get_rect(midtop=(x, 100))

    def update(self):
        self.rect.move_ip(0, 2)

        if self.rect.bottom >= self.game_screen.water.y:
            self.game_screen.water_rise(40)
            self.kill()

class FactsDisplay(pygame.sprite.Sprite):
    year = 2019
    sea_level = 0
    temperature = 0
    update_count = 0
    sea_level_delta = 3.3
    # temperature with added noise
    noisy_temperature = 0

    def __init__(self, game_screen, containers):
        pygame.sprite.Sprite.__init__(self, containers)
        self.image = pygame.Surface((game_screen.manager.screen_surface.get_rect().width, 100))
        self.rect = self.image.get_rect(topleft=(0, 0))

        self.year_font = pygame.font.SysFont("arial", game_screen.manager.screen_surface.get_rect().width // 20)
        self.info_font = pygame.font.SysFont("arial", game_screen.manager.screen_surface.get_rect().width // 40)
        
        self.game_screen = game_screen

        self.update_text()

    def update(self):
        self.update_count += 1
        if(self.update_count % 120 == 0):
            self.year += 1
            self.sea_level_delta += 0.1
            self.sea_level += self.sea_level_delta
            self.temperature += .019
            self.noisy_temperature = self.temperature + random.uniform(-.005, .005)
            
            self.update_text()

    def update_text(self):
        info_text = "Average sea level: +{:.2f}mm  Average temperature: +{:.4f}°C".format(self.sea_level, self.noisy_temperature)

        year_surface = self.year_font.render("Year " + str(self.year), True, (255, 255, 255))
        info_surface = self.info_font.render(info_text, True, (255, 255, 255))
        self.image.fill((35, 50, 74))
        self.image.blit(year_surface, (0, 0))
        self.image.blit(info_surface, (0, year_surface.get_rect().height + 10))