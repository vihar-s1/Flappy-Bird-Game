#!/usr/bin/env python

import pygame, random
from pygame.locals import *
    
__FPS = 32
__DISPLAY_WIDTH, __DISPLAY_HEIGHT = 289, 511

__DISPLAY = pygame.display.set_mode((__DISPLAY_WIDTH, __DISPLAY_HEIGHT))
__SPRITES = {}
    
def run():
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird With Python')


if __name__ == "__main__":
    run()