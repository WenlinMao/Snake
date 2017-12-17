#!/usr/bin/env python
# File Name: Snake
# Author: Wenlin Mao
# Date: Dec. 5, 2017

import pygame
import random
import os

WHITE = (0xff, 0xff, 0xff)
BLACK = (0, 0, 0)
GREEN = (0, 0xff, 0)
RED = (0xff, 0, 0)
LINE_COLOR = (0x33, 0x33, 0x33)
FPS = 30

#HARD_LEVEL = list(range(4, int(FPS/2), 2))
#age = 25

D_LEFT, D_RIGHT, D_UP, D_DOWN = 0, 1, 2, 3

# monologue for writing course which discuss the relationship between
# happiness and money
soliloquy = ['This is not \nenough, I need \nmore to be happy!\n',\
              'I got some money.\n It’s time to have\n' + 
                    'a new cellphone\n and a laptop. I am\n'+ 
                    ' happy with having \nthese properties.\n',\
              'I got enough \nmoney  to have a\n new car! I am \n' +
                    'excited about\n it!',\
              'I finally \ngot enough \nmoney for a new \n' + 
                    'house! These\n properties bring me \n'+
                    'a great deal of\n happiness!',\
              'Oh, I’ve got \nso many things, \nmoney seems not\n' + 
                    ' as attractive as\n before. But I \n' + 
                    'still need to \n gain more money\n to maintain \n' + 
                    'all things I \nhave. ',\
              'I am tired to\n afford all\nmaintenance fee,\n' + 
                    'and my health \nstatus is \ngetting worse\n' +
                    'right now. I\n am limited so \nmuch because\n' + 
                    'of money. ',\
              'My health status \nbecomes even \nworse, ' + 
                    'I need \nto be super \ncareful about \n'+
                    'maintaining my \nhealth.',\
              'Money can no\n' +
                    ' longer bring \nme happiness\n but better\n' + 
                    'health status can.']

pygame.init()
pygame.mixer.init()

# window width
WIDTH, HEIGHT = 500, 500

# extra sider for 200 width
SCREEN_WIDTH = WIDTH + 200

# with of snake
CELL_WIDTH = 20

# number of cell in with and height
CELL_WIDTH_NUM, CELL_HEIGHT_NUM = int(WIDTH / CELL_WIDTH),\
                                  int(HEIGHT / CELL_WIDTH)

# set canvas
screen = pygame.display.set_mode((SCREEN_WIDTH, HEIGHT))

# caption
pygame.display.set_caption("Snake")


# root folder
root_folder = os.path.dirname(__file__)

# folder for music
music_folder = os.path.join(root_folder, 'music')

# load music for background
background_music = pygame.mixer.music.load(os.path.join(music_folder,\
                                             'Adventure Meme.mp3'))

# play when snake eat food
eat_music = pygame.mixer.Sound(os.path.join(music_folder, 'armor-light.wav'))

# image folder
image_folder = os.path.join(root_folder, 'images')

# load background image
background_img = pygame.image.load(os.path.join(image_folder, 'back.png'))
# scale image to be same as window
background = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# load snake's head image
snake_head_img = pygame.image.load(os.path.join(image_folder, 'head.png'))
snake_head_img.set_colorkey(BLACK)
snake_body_img = pygame.image.load(os.path.join(image_folder, 'body.png'))
#snake_tail_img = pygame.image.load(os.path.join(image_folder, 'tail.png'))
# scale image to be same as cell
body = pygame.transform.scale(snake_body_img, (CELL_WIDTH, CELL_WIDTH))
#tail = pygame.transform.scale(snake_tail_img, (CELL_WIDTH, CELL_WIDTH))


# load food image
food_img = pygame.image.load(os.path.join(image_folder, 'DollarSign.jpg'))

# scale image to be same as cell
food = pygame.transform.scale(food_img, (CELL_WIDTH, CELL_WIDTH))

# specify font type
font_name = os.path.join(root_folder, 'font/font.ttc')


# game volume
#pygame.mixer.music.set_volume(0.4)

# play music infinite time
pygame.mixer.music.play(loops=-1)


# set timer
clock = pygame.time.Clock()

# set counter
counter = 0


# draw_grids: Draw Grid
def draw_grids():
    for i in range(CELL_WIDTH_NUM):
        pygame.draw.line(screen, LINE_COLOR,
                         (i * CELL_WIDTH, 0), (i * CELL_WIDTH, HEIGHT))

    for i in range(CELL_HEIGHT_NUM):
        pygame.draw.line(screen, LINE_COLOR,
                         (0, i * CELL_WIDTH), (WIDTH, i * CELL_WIDTH))

    pygame.draw.line(screen, WHITE,
                     (WIDTH, 0), (WIDTH, HEIGHT))


# draw_body: Draw snake body
def draw_body(status):

    for sb in status.snake_body[1:]:
        screen.blit(body, sb)

    if status.direction == D_LEFT:
        rot = 0
    elif status.direction == D_RIGHT:
        rot = 180
    elif status.direction == D_UP:
        rot = 270
    elif status.direction == D_DOWN:
        rot = 90

    new_head_img = pygame.transform.rotate(snake_head_img, rot)
    head = pygame.transform.scale(new_head_img, (CELL_WIDTH, CELL_WIDTH))
    screen.blit(head, status.snake_body[0])

    '''
    global tail

    
    if len(status.turn_pos) == 0:
        screen.blit(tail, status.snake_body[-1])
    elif status.turn_pos[0] == status.snake_body[-1]:
        new_tail_img = pygame.transform.rotate(snake_tail_img, rot)
        tail = pygame.transform.scale(new_tail_img,(CELL_WIDTH, CELL_WIDTH))
        screen.blit(tail, status.snake_body[-1])
        status.turn_pos.pop(0)
    else:
        screen.blit(tail, status.snake_body[-1])
    '''
    
    
# generate_food: draw food randomly
def generate_food(status=None):
    while True:

        # randomly generate position from 0 to height and 0 to width
        pos = (random.randint(0, CELL_WIDTH_NUM - 1),
               random.randint(0, CELL_HEIGHT_NUM - 1))

        if status is None:
            return pos

        # if there is no snake's body, return food position
        if not (pos[0] * CELL_WIDTH, pos[1] * CELL_WIDTH) in status.snake_body:
            return pos


# main body of the food
def draw_food(status):
    screen.blit(food, (status.food_pos[0] * CELL_WIDTH,
                      status.food_pos[1] * CELL_WIDTH, CELL_WIDTH, CELL_WIDTH))


# if the snake eat food successfully, we increase 
# the length of food by return true
def grow(status):
    if status.snake_body[0][0] == status.food_pos[0] * CELL_WIDTH and\
            status.snake_body[0][1] == status.food_pos[1] * CELL_WIDTH:
        # play music after eat
        eat_music.play()
        return True

    return False

# Class: status of game that used to keep track of each status
class GameStatus():
    def __init__(self):
        self.reset_game_status()

    # reset every status when initialize
    def reset_game_status(self):
        self.food_pos = generate_food()

        # originaly head left
        self.direction = D_LEFT
        self.game_is_over = True
        self.running = True
        self.age = 25
        self.money = 0

        #self.turn_pos = []

        # list of snake body, start in the middle of window
        self.snake_body = [(int(CELL_WIDTH_NUM / 2) * CELL_WIDTH,
                            int(CELL_HEIGHT_NUM / 2) * CELL_WIDTH)]
                           #(int((CELL_WIDTH_NUM / 2) + 1) * CELL_WIDTH,
                            #int(CELL_HEIGHT_NUM / 2) * CELL_WIDTH)]


# present text to game
def show_text(surf, text, size, x, y, color=WHITE):

    global font_name

    # specify size of printed font
    font_print = pygame.font.Font(font_name, size)

    # 2D array where each row is a list of words.
    words = text.splitlines()  
    for line in words:

        text_surface = font_print.render(line, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

        y += 1.5 * CELL_WIDTH # Start on new row.


def show_welcome(screen):

    show_text(screen, 'Snake', 30, WIDTH / 2, HEIGHT / 2)


def show_moneys(screen, status):

    # age field of the game in purpose of expressing the relationship
    # of happiness and age
    show_text(screen, u'Age: {}'.format(status.age), CELL_WIDTH,
        WIDTH + CELL_WIDTH * 5, CELL_WIDTH * 3)

    show_text(screen, u'Money: ${}'.format(status.money), CELL_WIDTH,
        WIDTH + CELL_WIDTH * 5, CELL_WIDTH * 5)

    # show soliloquy according to the condition
    score = status.money / 10000

    '''
    if score == 1: 
        show_text(screen, soliloquy[0]\
                    , CELL_WIDTH, WIDTH + CELL_WIDTH * 5\
                    , CELL_WIDTH * 9)
    elif score == 2:
        show_text(screen, soliloquy[1]\
                    , CELL_WIDTH, WIDTH + CELL_WIDTH * 5\
                    , CELL_WIDTH * 9)
    elif score == 3:
        show_text(screen, soliloquy[2]\
                    , CELL_WIDTH, WIDTH + CELL_WIDTH * 5\
                    , CELL_WIDTH * 9)
    elif score == 4:
        show_text(screen, soliloquy[3]\
                    , CELL_WIDTH, WIDTH + CELL_WIDTH * 5\
                    , CELL_WIDTH * 9)
    elif score == 5:
        show_text(screen, soliloquy[4]\
                    , CELL_WIDTH, WIDTH + CELL_WIDTH * 5\
                    , CELL_WIDTH * 9)
    elif score == 6:
        show_text(screen, soliloquy[5]\
                    , CELL_WIDTH, WIDTH + CELL_WIDTH * 5\
                    , CELL_WIDTH * 9)
    elif score == 7:
        show_text(screen, soliloquy[6]\
                    , CELL_WIDTH, WIDTH + CELL_WIDTH * 5\
                    , CELL_WIDTH * 9)
    elif score == 8:
        show_text(screen, soliloquy[7]\
            , CELL_WIDTH, WIDTH + CELL_WIDTH * 5\
            , CELL_WIDTH * 9)
    '''
        
    show_text(screen, soliloquy[int((score - 1)/10)]\
                    , CELL_WIDTH, WIDTH + CELL_WIDTH * 5\
                    , CELL_WIDTH * 9)

draw_grids()
pygame.display.update()

#initialize status object for this game
status = GameStatus()

# if the running status is true, keep run snake
while status.running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status.running = False
            pygame.display.quit()
            pygame.quit()
            break
            
        elif event.type == pygame.KEYDOWN:    
            # if game is over, press any key to restart
            if status.game_is_over:
                # reset game status
                status.reset_game_status()
                status.game_is_over = False
                continue


            # set status according to key pressed
            if event.key == pygame.K_UP and status.direction != D_DOWN:
                status.direction = D_UP
            elif event.key == pygame.K_DOWN and status.direction != D_UP:
                status.direction = D_DOWN
            elif event.key == pygame.K_LEFT and status.direction != D_RIGHT:
                status.direction = D_LEFT
            elif event.key == pygame.K_RIGHT and status.direction != D_LEFT:
                status.direction = D_RIGHT
            # if the key is esc, end the game
            elif event.key == pygame.K_ESCAPE:
                status.running = False
                pygame.display.quit()
                pygame.quit()
                break

    if status.running == False:
        break

    if status.game_is_over:
        show_welcome(screen)
        pygame.display.update()
        continue

    # use speed as FPS / 10
    # TODO: two keydown in one surface update may cause snake's head
    # turn 180 degree and hit its body
    if counter % int(FPS / 10) == 0:
        # position of the tail of the snake for future grow
        last_pos = status.snake_body[-1]

        #status.turn_pos.append(status.snake_body[0])

        # update the snake's body
        for i in range(len(status.snake_body) - 1, 0, -1):
            status.snake_body[i] = status.snake_body[i - 1]

        # chagne head position
        if status.direction == D_UP:
            status.snake_body[0] = (
                status.snake_body[0][0],
                status.snake_body[0][1] - CELL_WIDTH)
        elif status.direction == D_DOWN:
            status.snake_body[0] = (
                status.snake_body[0][0],
                status.snake_body[0][1] + CELL_WIDTH)
        elif status.direction == D_LEFT:
            status.snake_body[0] = (
                status.snake_body[0][0] - CELL_WIDTH,
                status.snake_body[0][1])
        elif status.direction == D_RIGHT:
            status.snake_body[0] = (
                status.snake_body[0][0] + CELL_WIDTH,
                status.snake_body[0][1])

    
        if status.snake_body[0][0] < 0 or status.snake_body[0][0] >= WIDTH or\
                status.snake_body[0][1] < 0 \
                or status.snake_body[0][1] >= HEIGHT:
            # gameover if touch the wall
            status.game_is_over = True
            show_text(screen, 'You died and lost \nall your money', \
                        30, WIDTH / 2, HEIGHT / 2)
            pygame.display.update()
            pygame.time.delay(2000)

        # gameover if hit itself
        for sb in status.snake_body[1: ]:
            if sb == status.snake_body[0]:
                status.game_is_over = True
                if status.money >= 800000:
                    show_text(screen, 'You will die no matter \nhow many' + \
                               ' money you have', 30, WIDTH / 2, HEIGHT / 2)
                else:
                    show_text(screen, 'You died and lost\n' +
                                'all your money', 30, WIDTH / 2, HEIGHT / 2)

                pygame.display.update()
                pygame.time.delay(2000)

        # if grow return's true, increase the body length
        got_food = grow(status)

        # gerenate food after getting new food
        if got_food:

            status.age += 1
            status.money += 10000
            status.food_pos = generate_food(status)

            # length after eat one food
            for i in range(5):
                status.snake_body.append(last_pos)

            #status.age = HARD_LEVEL[min(int(len(status.snake_body) / 10),
                                      #len(HARD_LEVEL) - 1)]

    # screen.fill(BLACK)
    pygame.draw.rect(screen, BLACK, (WIDTH, 0, SCREEN_WIDTH - WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    draw_grids()

    # update snake body
    draw_body(status)

    # update food 
    draw_food(status)

    # update money
    show_moneys(screen, status)

    # counter add by one
    counter += 1
    pygame.display.update()

pygame.quit()