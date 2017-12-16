#!/usr/bin/env python
# File Name: Snake
# Author: Wenlin Mao

# import packages
import pygame, random, sys
from pygame.locals import *

pygame.init()

window_size = (500, 500)

# size of cell
cell_size = [window_size[0] / 10, window_size[1] / 10]


# resizable canvas
screen = pygame.display.set_mode(window_size, 0, 32)

# title
pygame.display.set_caption("Snake")

background = pygame.Surface(window_size)
background.fill((255, 255, 255))

screen.blit(background, (0,0))

main()

class money(object):

    """
    initialize money
    """
    def __init__(self):

        # set x and y of money to be random value in the windown
        self.x = random.randint(10, window_size[0] - 10)
        self.y = random.randint(10, window_size[1] - 10)

        # set image of money to be DollarSign
        self.image = pygame.image.load("DollarSign").convert()

    """
    get money image
    """
    def get_image(self):
        return self.image

    """
    get money position
    """
    def get_position(self):
        return [self.x, self.y]

def main():

    while True:
        run_game()
        game_over()

def run_game():

    # main loop
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if event.type == KEYDOWN:
                if event.type == K_ESCAPE:
                    exit()


        x, y = pygame.mouse.get_pos()
        cursor = pygame.Surface((80, 80))
        cursor.fill((0, 0, 0))

        x-= cursor.get_width() / 2
        y-= cursor.get_height() / 2
        screen.blit(cursor, (x, y))

        pygame.display.update()

    return

def game_over():
    return
