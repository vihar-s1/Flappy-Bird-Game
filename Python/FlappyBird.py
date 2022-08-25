#!/usr/bin/env python

import pygame, random
from pygame.locals import *
    
    
#! GLOBAL VARIABLES
__FPS = 32
__DISPLAY_WIDTH, __DISPLAY_HEIGHT = 289, 511

__DISPLAY = pygame.display.set_mode((__DISPLAY_WIDTH, __DISPLAY_HEIGHT))


#. Dictionary containing refernce to all the sprites to be used in the game
__SPRITES = {
    'player' : pygame.image.load('./Sprites/bird.png').convert_alpha(),
    'background' : pygame.image.load('./Sprites/background.png').convert_alpha(),
    
    'message' : pygame.image.load('./Sprites/message.png').convert_alpha(),
    'base' : pygame.image.load('./Sprites/base.png').convert_alpha(),
    
    'pipe' : (pygame.transform.rotate(pygame.image.load('./Sprites/pipe.png').convert_alpha(), 180),
              pygame.image.load('./Sprites/pipe.png').convert_alpha(),
              ),
        
    'numbers' : (pygame.image.load('./Sprites/0.png').convert_alpha(),
                 pygame.image.load('./Sprites/1.png').convert_alpha(),
                 pygame.image.load('./Sprites/2.png').convert_alpha(),
                 pygame.image.load('./Sprites/3.png').convert_alpha(),
                 pygame.image.load('./Sprites/4.png').convert_alpha(),
                 pygame.image.load('./Sprites/5.png').convert_alpha(),
                 pygame.image.load('./Sprites/6.png').convert_alpha(),
                 pygame.image.load('./Sprites/7.png').convert_alpha(),
                 pygame.image.load('./Sprites/8.png').convert_alpha(),
                 pygame.image.load('./Sprites/9.png').convert_alpha(),
                 )
}
  
#. Dictionary containing the audio files to be used in the game
__AUDIO = {}
  

def __welcomScreen():  
    '''Shows welcome image on the screen'''
    playerx, playery = __DISPLAY_WIDTH // 5, (__DISPLAY_HEIGHT - __SPRITES['player'].get_height()) // 2
    messagex, messagey = 1
    
def run():
    '''Starts running the game by setting up pygame window and running the mainloop '''
    pygame.init()
    global __FPSCLOCK
    __FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird With Python')

    __AUDIO['die.wav'] = pygame.mixer.Sound('./audio/die.wav')
    __AUDIO['hit.wav'] = pygame.mixer.Sound('./audio/hit.wav')
    __AUDIO['point.wav'] = pygame.mixer.Sound('./audio/point.wav')
    __AUDIO['swoosh.wav'] = pygame.mixer.Sound('./audio/swoosh.wav')
    __AUDIO['wing.wav'] = pygame.mixer.Sound('./audio/wing.wav')

if __name__ == "__main__":
    run()
    