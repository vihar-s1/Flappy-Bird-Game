#!/usr/bin/env python

from pickle import GLOBAL
import pygame, random, sys
from pygame.locals import *
from os import path

#-------------------------------------------------------------------------------------------------#
#------------------- DEFINING RESOURCE LOCATIONS FOR MAKING IT CONVERTIBLE TO EXE ----------------#
#-------------------------------------------------------------------------------------------------#
def resource_path(relative_path: str):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception as e:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)

#-------------------------------------------------------------------------------------------------#
#--------------------------------------- GLOBAL VARIABLES ----------------------------------------#
#-------------------------------------------------------------------------------------------------#

__FPS = 32
__DISPLAY_WIDTH, __DISPLAY_HEIGHT = 289, 511
__HIGH_SCORE = 0

__DISPLAY = pygame.display.set_mode((__DISPLAY_WIDTH, __DISPLAY_HEIGHT))
__GROUNDY = __DISPLAY_HEIGHT * 0.8
__PIPE_GAP = __DISPLAY_HEIGHT // 3  # intial distance between two pipes
__PIPE_MIN_GAP = __DISPLAY_HEIGHT // 5 # minimum distance between two pipes
__PIPE_CLOSING_RATE = -10

PLAYER_PATH =  resource_path('Sprites/bird.png')
BACKGROUND_PATH = resource_path('Sprites/background.png')
PIPE_PATH = resource_path('Sprites/pipe.png ')

__PIPEX_SPEED = -4
__PIPEX_MINSPEED = -10
__PIPEX_ACC = -1
    

#-------------------------------------------------------------------------------------------------#
#------------------------ DICTIONARIES CONTAINING SPRITES AND AUDIO FILES ------------------------#
#-------------------------------------------------------------------------------------------------#

#. Dictionary containing refernce to all the sprites to be used in the game
__SPRITES = {
    'player' : pygame.image.load(PLAYER_PATH).convert_alpha(),
    'background' : pygame.image.load(BACKGROUND_PATH).convert_alpha(),
    
    'message' : pygame.image.load( resource_path('Sprites/message.png') ).convert_alpha(),
    'base' : pygame.image.load( resource_path('Sprites/base.png') ).convert_alpha(),
    
    'highScore' : pygame.image.load( resource_path('Sprites/highScore.png') ).convert_alpha(),
    
    'pipe' : (pygame.transform.rotate(pygame.image.load( resource_path(PIPE_PATH) ).convert_alpha(), 180),
              pygame.image.load(PIPE_PATH).convert_alpha(),
              ),
        
    'numbers' : (pygame.image.load( resource_path('Sprites/0.png') ).convert_alpha(),
                 pygame.image.load( resource_path('Sprites/1.png') ).convert_alpha(),
                 pygame.image.load( resource_path('Sprites/2.png') ).convert_alpha(),
                 pygame.image.load( resource_path('Sprites/3.png') ).convert_alpha(),
                 pygame.image.load( resource_path('Sprites/4.png') ).convert_alpha(),
                 pygame.image.load( resource_path('Sprites/5.png') ).convert_alpha(),
                 pygame.image.load( resource_path('Sprites/6.png') ).convert_alpha(),
                 pygame.image.load( resource_path('Sprites/7.png') ).convert_alpha(),
                 pygame.image.load( resource_path('Sprites/8.png') ).convert_alpha(),
                 pygame.image.load( resource_path('Sprites/9.png') ).convert_alpha(),
                 )
}
  
#. Dictionary containing the audio files to be used in the game
__AUDIO = {}
  

#--------------------------------------------------------------------------------------------------#
#----------------------------------------- GAME FUNCTIONS -----------------------------------------#
#--------------------------------------------------------------------------------------------------#

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
            elif event.type == KEYDOWN and event.key in [K_SPACE, K_UP]:
                return
            else:
                __DISPLAY.blit(__SPRITES['background'], (0, 0))
                __DISPLAY.blit(__SPRITES['player'], (playerx, playery))
                __DISPLAY.blit(__SPRITES['message'], (messagex, messagey))
                __DISPLAY.blit(__SPRITES['base'], (basex, __GROUNDY))
                
                # Displaying the high score
                scoreDigits = list(map(int, list(str(__HIGH_SCORE))))
                
                width = __SPRITES['highScore'].get_width()
                
                for digit in scoreDigits:
                    width += __SPRITES['numbers'][digit].get_width()
                    
                Xoffset = (__DISPLAY_WIDTH - width) // 2
                
                        
                __DISPLAY.blit(__SPRITES['highScore'], (Xoffset, __DISPLAY_HEIGHT * 0.88))
                Xoffset += __SPRITES['highScore'].get_width()
                
                for digit in scoreDigits:
                    __DISPLAY.blit(__SPRITES['numbers'][digit], (Xoffset, __DISPLAY_HEIGHT * 0.88))
                    Xoffset += __SPRITES['numbers'][digit].get_width()
        
                pygame.display.update()
                __FPSCLOCK.tick(__FPS)
    

def __generatePipe():
    '''
    Generates positional coordinate for the upper and lower pipes
    '''
    # need declare that __PIPE_GAP is a global variable before changing inside function
    global __PIPE_GAP, __PIPEX_SPEED
     
    pipeHeight = __SPRITES['pipe'][0].get_height()
    y2 = __PIPE_GAP + random.randrange(0, int(__DISPLAY_HEIGHT - __SPRITES['base'].get_height() - 1.2*__PIPE_GAP))
    pipeX = __DISPLAY_WIDTH + (2 * abs( __PIPEX_SPEED))
    y1 = pipeHeight - y2 + __PIPE_GAP
    
    __PIPE_GAP = max(__PIPE_MIN_GAP, __PIPE_GAP + __PIPE_CLOSING_RATE)
    __PIPEX_SPEED = max(__PIPEX_MINSPEED, __PIPEX_SPEED + __PIPEX_ACC)
    
    pipes = [
        {'x':pipeX, 'y':-y1}, # Upper
        {'x':pipeX, 'y':y2} # Lower
    ]
    return pipes


def __isCollision(playerX, playerY, upperPipes, lowerPipes):
    if playerY >= __GROUNDY - __SPRITES['player'].get_height() or playerY < 0:
        __AUDIO['hit'].play()
        return True
    
    pipeHeight = __SPRITES['pipe'][0].get_height()
        
    for pipe in upperPipes:    
        if playerY < pipeHeight + pipe['y'] and (abs(playerX - pipe['x']) < __SPRITES['player'].get_width()):
            __AUDIO['hit'].play()
            return True
    
    for pipe in lowerPipes:   
        if playerY + __SPRITES['player'].get_height() > pipe['y'] and (abs(playerX - pipe['x']) < __SPRITES['player'].get_width()):
            __AUDIO['hit'].play()
            return True
        
    return False


def __mainGame():
    global __HIGH_SCORE, __PIPE_GAP, __PIPEX_SPEED
    score = 0
    playerX = __DISPLAY_WIDTH // 5
    playerY = __DISPLAY_HEIGHT // 2
    baseX = 0
    __PIPE_GAP = __DISPLAY_HEIGHT // 3 # Reseting the pipe gap to original distance

    newPipe1 = __generatePipe()
    
    
    upperPipes = [
        {'x': __DISPLAY_WIDTH + 50 * abs(__PIPEX_SPEED), 'y': newPipe1[0]['y']},
    ]
    lowerPipes = [
        {'x': __DISPLAY_WIDTH + 50 * abs(__PIPEX_SPEED), 'y': newPipe1[1]['y']},
    ]
    
    __PIPEX_SPEED, playerY_speed = -4, -9
    playerY_max = 10
    playerY_min = -8
    playerY_acc = 1
    
    playerFlapping_speed = -15 # velocity while flapping
    playerFlapped = False # True when the bird is flappnig
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key in [K_SPACE, K_UP]):
                if playerY > 0:
                    playerY_speed += playerFlapping_speed
                    playerFlapped = True
                    __AUDIO['wing'].play()
        
        crashed = __isCollision(playerX, playerY, upperPipes, lowerPipes)
        if crashed:
            return

        playerMidPos = playerX + __SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + __SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + abs(__PIPEX_SPEED):
                score += 1
                
                __HIGH_SCORE = max(__HIGH_SCORE, score)
                __AUDIO['point'].play()
        
        if playerY_speed < playerY_max and not playerFlapped:
            playerY_speed += playerY_acc
        
        if playerFlapped:
            playerFlapped = False
        
        playerHeight = __SPRITES['player'].get_height()
        playerY += min(playerY_speed, __GROUNDY - playerY - playerHeight)
        
            
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += __PIPEX_SPEED
            lowerPipe['x'] += __PIPEX_SPEED
        
        # add a new pipe when the first is about to cross the leftmost part of the screen
        # if 0 < upperPipes[0]['x'] < 5:
        #     newPipe = __generatePipe()
        #     upperPipes.append(newPipe[0])
        #     lowerPipes.append(newPipe[1])
        
        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -__SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
            # Add a new pipe after removing the leftmost pipe.
            newPipe = __generatePipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])
            
        __DISPLAY.blit(__SPRITES['background'], (0, 0))
        
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            __DISPLAY.blit( __SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']) )
            __DISPLAY.blit( __SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']) )
        
        __DISPLAY.blit(__SPRITES['base'], (baseX, __GROUNDY))
        __DISPLAY.blit(__SPRITES['player'], (playerX, playerY))
        
        # displaying the score of the game
        scoreDigits = list(map(int, list(str(score))))
        width = 0
        for digit in scoreDigits:
            width += __SPRITES['numbers'][digit].get_width()
            
        Xoffset = (__DISPLAY_WIDTH - width) // 2
        for digit in scoreDigits:
            __DISPLAY.blit(__SPRITES['numbers'][digit], (Xoffset, __DISPLAY_HEIGHT * 0.12))
            Xoffset += __SPRITES['numbers'][digit].get_width()
        
        pygame.display.update()   
        __FPSCLOCK.tick(__FPS)        

 
def run():
    '''Starts running the game by setting up pygame window and running the mainloop '''
    pygame.init()
    global __FPSCLOCK
    __FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird With Python')

    __AUDIO['die'] = pygame.mixer.Sound( resource_path('./audio/die.wav') )
    __AUDIO['hit'] = pygame.mixer.Sound( resource_path('./audio/hit.wav') )
    __AUDIO['point'] = pygame.mixer.Sound( resource_path('./audio/point.wav') )
    __AUDIO['swoosh'] = pygame.mixer.Sound( resource_path('./audio/swoosh.wav') )
    __AUDIO['wing'] = pygame.mixer.Sound( resource_path('./audio/wing.wav') )

    while True:
        __welcomScreen()
        __mainGame()

if __name__ == "__main__":
    run()
    