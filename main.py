# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018

@author: zou
"""

import pygame
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT

from os.path import exists

from game import Game

# define colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

green = pygame.Color(0, 200, 0)
bright_green = pygame.Color(0, 255, 0)
red = pygame.Color(200, 0, 0)
bright_red = pygame.Color(255, 0, 0)
blue = pygame.Color(32, 178, 170)
bright_blue = pygame.Color(32, 200, 200)
yellow = pygame.Color(255, 205, 0)
bright_yellow = pygame.Color(255, 255, 0)


# game instance
game = Game()
rect_len = game.settings.rect_len
snake = game.snake
pygame.init() # initialize pygame library

fpsClock = pygame.time.Clock()     # keep track of time

# set up window
screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15))
pygame.display.set_caption('Gluttonous')

# load sound
crash_sound = pygame.mixer.Sound('./sound/crash.wav')


def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, x, y, color=black, font_size=50):
    large_text = pygame.font.SysFont('comicsansms', font_size)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    # pygame.display.update()


def button(msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # if clicked inside the button area
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            if parameter != None:
                action(parameter)
            else:
                action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    smallText = pygame.font.SysFont('comicsansms', 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(TextSurf, TextRect)


def quitgame():
    pygame.quit()
    quit()


def crash():
    pygame.mixer.Sound.play(crash_sound)
    message_display('crashed', game.settings.width / 2 * 15, game.settings.height / 3 * 15, white)
    time.sleep(1)


def back_to_main_window():
    global back_button_pressed
    back_button_pressed = True

def draw_score_board():
    
    board_surf = pygame.Surface((game.settings.height, game.settings.width))
    # screen.fill(yellow);
    screen.blit(board_surf, (0, 0))

    # draw score texts
    smallText = pygame.font.SysFont('comicsansms', 30)
    TextSurf, TextRect = text_objects("Top 5 Scores:", smallText)
    TextRect.center = (game.settings.width / 2 * 15, game.settings.height / 4 * 10)
    screen.blit(TextSurf, TextRect)

    top_5_scores = ['None'] * 5
    
    # draw score numbers
    for i in range(5):
        # read top 5 score from file

        if exists("score.txt"):
            with open('score.txt', 'r') as f:
                lines = f.readlines()
                lines.sort(reverse=True)
                for j in range(5):
                    if j >= len(lines): break
                    top_5_scores[j] = lines[j].strip('\n')
            TextSurf, TextRect = text_objects(f'{str(i + 1)}. {top_5_scores[i]}', smallText)
            if top_5_scores[i] == 'None':
                TextRect.center = (game.settings.width / 2 * 12, game.settings.height / 4 * 13 + (i + 1) * 35)
            else:
                TextRect.center = (game.settings.width / 2 * 10, game.settings.height / 4 * 13 + (i + 1) * 35)

        screen.blit(TextSurf, TextRect)

def display_scoreboard(fps=10):
    global back_button_pressed
    back_button_pressed = False

    # background_image = pygame.image.load('./images/Aatrox_7.jpg')
    background_image = pygame.image.load('./images/Syndra_4.jpg')

    while not back_button_pressed: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # screen.fill(black)
        screen.blit(background_image, (-300, -80))
        draw_score_board()
        button("Back", 0, 0, 80, 40, green, bright_green, back_to_main_window)  # create a back button
        # pygame.event.pump() already included in pygame.event.get()
        pygame.display.flip()   # updates screen

def initial_interface():
    intro = True

    # draw background image to main screen
    background_image = pygame.image.load('./images/bgimage.webp')
    while intro:

        # if close button is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(white)
        screen.blit(background_image, (-700, -175))
        message_display('Gluttonous', game.settings.width / 2 * 15, game.settings.height / 4 * 15)

        button('Go!', 50, 240, 80, 40, green, bright_green, game_loop, 'human')
        button("Scoreboard", 155, 240, 120, 40, blue, bright_blue, display_scoreboard)
        button('Quit', 300, 240, 80, 40, red, bright_red, quitgame)

        pygame.display.flip()
        pygame.time.Clock().tick(30)

def skin_manager(skinName):
    global play_button_pressed
    play_button_pressed = True

    game.snake.setSkin(skinName)  # skin skin for the sprite

def display_settings():
    global play_button_pressed
    global back_button_pressed
    play_button_pressed = False
    back_button_pressed = False

    background_image = pygame.image.load('./images/TwistedFate_3.jpg')
    # background_image = pygame.image.load('./images/Syndra_4.jpg')
    while not play_button_pressed and not back_button_pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.blit(background_image, (-300, -80))


        # pick a skin message
        message_display('Pick a skin:', game.settings.width / 2 * 15, game.settings.height / 4 * 15, black, 40)

        # draw a button for each skin
        button('Fire', game.settings.width / 2 * 10.5, game.settings.height / 4 * 21, 120, 45, red, bright_red, skin_manager, 'Fire')
        button('Wind', game.settings.width / 2 * 10.5, game.settings.height / 4 * 30, 120, 45, blue, bright_blue, skin_manager, 'Wind')
        button('Lightning', game.settings.width / 2 * 10.5, game.settings.height / 4 * 39, 120, 45, yellow, bright_yellow, skin_manager, 'Lightning')

        button("Back", 0, 0, 80, 40, green, bright_green, back_to_main_window)  # create a back button
        # pygame.event.pump() already included in pygame.event.get()
        pygame.display.flip()   # updates screen
    
    # determine which button was pressed
    return play_button_pressed

def save_score(score):
    # save score in a file
    with open('score.txt', 'a') as f:
        f.write(str(score) + '\n')

def game_loop(player, fps=10):
    condition = display_settings()
    if not condition: return    # this means that back button was pressed instead of play button

    game.restart_game()

    # background image of game
    background_image = pygame.image.load('./images/bgimage.webp')

    while not game.game_end():

        pygame.event.pump() # handle internal actions

        move = human_move() # integer representing direction
        # {0 : 'up',
        #   1 : 'down',
        #   2 : 'left',
        #   3 : 'right'}
        # fps = 30

        game.do_move(move)

        screen.fill(black)
        screen.blit(background_image, (-400, -250))

        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(white, screen)

        pygame.display.flip()   # updates screen

        fpsClock.tick(fps)

    crash()
    save_score(game.snake.score)


def human_move():
    direction = snake.facing

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        # if oen of the arrow keys are pressed, or escape key is pressed
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT or event.key == ord('d'):
                direction = 'right'
            if event.key == K_LEFT or event.key == ord('a'):
                direction = 'left'
            if event.key == K_UP or event.key == ord('w'):
                direction = 'up'
            if event.key == K_DOWN or event.key == ord('s'):
                direction = 'down'
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    move = game.direction_to_int(direction)
    return move


if __name__ == "__main__":
    initial_interface()
