#!/usr/bin/env python

from os import getrandom
from subprocess import PIPE
import pygame, random, sys
from pygame.locals import *
    
    
#! GLOBAL VARIABLES
__FPS = 32
__DISPLAY_WIDTH, __DISPLAY_HEIGHT = 289, 511

__DISPLAY = pygame.display.set_mode((__DISPLAY_WIDTH, __DISPLAY_HEIGHT))
__GROUNDY = __DISPLAY_HEIGHT * 0.8

PLAYER_PATH =  'Sprites/bird.png'
BACKGROUND_PATH = 'Sprites/background.png'
PIPE_PATH = 'Sprites/pipe.png '

#. Dictionary containing refernce to all the sprites to be used in the game
__SPRITES = {
    'player' : pygame.image.load(PLAYER_PATH).convert_alpha(),
    'background' : pygame.image.load(BACKGROUND_PATH).convert_alpha(),
    
    'message' : pygame.image.load('Sprites/message.png').convert_alpha(),
    'base' : pygame.image.load('Sprites/base.png').convert_alpha(),
    
    'pipe' : (pygame.transform.rotate(pygame.image.load(PIPE_PATH).convert_alpha(), 180),
              pygame.image.load(PIPE_PATH).convert_alpha(),
              ),
        
    'numbers' : (pygame.image.load('Sprites/0.png').convert_alpha(),
                 pygame.image.load('Sprites/1.png').convert_alpha(),
                 pygame.image.load('Sprites/2.png').convert_alpha(),
                 pygame.image.load('Sprites/3.png').convert_alpha(),
                 pygame.image.load('Sprites/4.png').convert_alpha(),
                 pygame.image.load('Sprites/5.png').convert_alpha(),
                 pygame.image.load('Sprites/6.png').convert_alpha(),
                 pygame.image.load('Sprites/7.png').convert_alpha(),
                 pygame.image.load('Sprites/8.png').convert_alpha(),
                 pygame.image.load('Sprites/9.png').convert_alpha(),
                 )
}
  
#. Dictionary containing the audio files to be used in the game
__AUDIO = {}
  

def __welcomScreen():  
    '''Shows welcome image on the screen'''
    playerx = __DISPLAY_WIDTH // 6
    playery = (__DISPLAY_HEIGHT - __SPRITES['player'].get_height()) // 2
    messagex = (__DISPLAY_WIDTH - __SPRITES['message'].get_width()) // 2
    messagey =  int(__DISPLAY_HEIGHT * 0.13)
    basex = 0
    
    while True:
        for event in pygame.event.get():
            # if user clicks on button X
            # or a key is pressed and the key is escape key
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            # if the user presses the space key, start game
            elif event.type == KEYDOWN and event.key == K_SPACE:
                return
            else:
                __DISPLAY.blit(__SPRITES['background'], (0, 0))
                __DISPLAY.blit(__SPRITES['player'], (playerx, playery))
                __DISPLAY.blit(__SPRITES['message'], (messagex, messagey))
                __DISPLAY.blit(__SPRITES['base'], (basex, __GROUNDY))
                pygame.display.update()
                __FPSCLOCK.tick(__FPS)
    

def generatePipe():
    '''
    Generates positional coordinate for the upper and lower pipes
    '''
    pipeHeight = __SPRITES['pipe'][0].get_height()
    offset = __DISPLAY_HEIGHT // 3
    y2 = offset + random.randrange(0, int(__DISPLAY_HEIGHT - __SPRITES['base'].get_height() - 1.2*offset))
    pipeX = __DISPLAY_WIDTH + 10
    y1 = pipeHeight - y2 + offset
    
    pipes = [
        {'x':pipeX, 'y':-y1}, # Upper
        {'x':pipeX, 'y':y2} # Lower
    ]


def __mainGame():
    score = 0
    playerX = __DISPLAY_WIDTH // 5
    playerY = __DISPLAY_HEIGHT // 2
    baseX = 0

    newPipe1 = generatePipe()
    newPipe2 = generatePipe()
    
    upperPipes = [
        {'x': __DISPLAY_WIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': __DISPLAY_HEIGHT + 200 + (__DISPLAY_WIDTH//2), 'y': newPipe2[1]['y']}
    ]
    lowerPipes = [
        {'x': __DISPLAY_WIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': __DISPLAY_HEIGHT + 200 + (__DISPLAY_WIDTH//2), 'y': newPipe2[1]['y']}
    ]
    
    pipeX_Speed, playerY_speed = -4, -9
    playerMaxY = 10
    playerMinY = -8
    playerAccY = 1
    
    playerFlapping_speed = -8 # velocity while flapping
    playerFlapped = False # True when the bird is flappnig
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key in [K_SPACE, K_UP]):
                if playerY > 0:
                    playerVelY = playerFlapping_speed
                    playerFlapped = True
                    __AUDIO['wing'].play()
        
        crashed = isCollision(playerX, playerY, upperPipes, lowerPipes)
        if crashed:
            return

        playerMidPos = playerX + __SPRITES['player'].get_width/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + __SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"score: {score}")
            __AUDIO['point'].play()
        
        if playerVelY < playerMaxY and not playerFlapped:
            playerVelY += playerAccY
        
        if playerFlapped:
            playerFlapped = False
        
        playerHeight = __SPRITES['player'].get_height()
        playerY += min(playerVelY, __GROUNDY - playerY - playerHeight)
            
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeX_Speed
            lowerPipe['x'] += pipeX_Speed
        
        # add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = generatePipe()
            upperPipes.append(newPipe[0])
            lowerPipe.append(newPipe[1])
        
        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -__SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
            
        __DISPLAY.blit(__SPRITES['background'], (0, 0))
        __DISPLAY.blit(__SPRITES['base'], (baseX, __GROUNDY))
        __DISPLAY.blit(__SPRITES['player'], (playerX, playerY))
        
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            __DISPLAY.blit( __SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']) )
            __DISPLAY.blit( __SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']) )
        
            
            

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

    while True:
        __welcomScreen()
        __mainGame()

if __name__ == "__main__":
    run()
    