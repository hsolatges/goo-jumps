import pygame, sys
from pygame.locals import *
from config import Config
from modules.sprites import Element, Axe
#from utils import to_tl_coordinates

cfg = Config
pygame.init()
DISPLAYSURF = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
pygame.display.set_caption(cfg.TITLE)

# Dealing with sprites
sprites = pygame.sprite.Group()
yaxe = Axe(DISPLAYSURF)
sprites.add(yaxe)

goo = Element((0, 2 * cfg.SCREEN_HEIGHT / 4), DISPLAYSURF)
sprites.add(goo)

STOP = False
while not STOP:
    for event in pygame.event.get():
        if event.type == QUIT:
            STOP = True
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            match event.button:
                case 1:  # Left click
                    goo.jump('left')
                case 3:  # Right click
                    goo.jump('right')
                case 2:
                    goo.setterTest('x')
                    goo.setterTest('y')

    sprites.update()
    DISPLAYSURF.fill((0, 0, 255))
    sprites.draw(DISPLAYSURF)
    pygame.display.update()
    pygame.time.Clock().tick(cfg.FPS)
