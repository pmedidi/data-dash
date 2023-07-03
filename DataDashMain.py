import pygame
import random
import math
from sys import exit
from enum import Enum

# initialize the game
pygame.init()

display_height = 600
display_width = display_height + 100
border = 10
(width, height) = (display_width, display_height)
title_font = pygame.font.Font('font/Pixeltype.ttf', 100)

class States(Enum):
    INTRO = 0
    SELECTION = 1
    ARRAYLIST = 2

class Player(pygame.sprite.Sprite):
    def __init__(self):  # constructor
        super().__init__()
        # initialize my sprites images to variables
        right_cat = pygame.image.load('images/player/RightCat.png').convert_alpha()
        right_cat = pygame.transform.scale2x(right_cat)
        left_cat = pygame.image.load('images/player/LeftCat.png').convert_alpha()
        left_cat = pygame.transform.scale2x(left_cat)
        down_cat = pygame.image.load('images/player/DownCat.png').convert_alpha()
        down_cat = pygame.transform.scale2x(down_cat)
        up_cat = pygame.image.load('images/player/UpCat.png').convert_alpha()
        up_cat = pygame.transform.scale2x(up_cat)

        self.sprite_directions = [right_cat, left_cat, down_cat, up_cat]
        self.sprite_index = 0

        self.image = self.sprite_directions[self.sprite_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.sprite_index = 3
            if self.rect.y > 0:
                self.rect.y -= 300 * dt
                if self.rect.top < border:
                    self.rect.y = border
        if keys[pygame.K_DOWN]:
            self.sprite_index = 2
            if self.rect.bottom < height - border:
                self.rect.y += 300 * dt
                if height - border <= self.rect.bottom:
                    self.rect.bottom = height - border
        if keys[pygame.K_LEFT]:
            self.sprite_index = 1
            if self.rect.x > 0:
                self.rect.x -= 300 * dt
                if self.rect.x < 0:
                    self.rect.x = 0
        if keys[pygame.K_RIGHT]:
            self.sprite_index = 0
            if self.rect.right < width - border:
                self.rect.x += 300 * dt
                if self.rect.x >= width - border:
                    self.rect.x = width - border
        # updates cat image
        self.image = self.sprite_directions[self.sprite_index]

    def update(self):
        self.player_input()

def display_intro():
    screen.fill((178, 190, 181))
    title_text = title_font.render('Data Dash', False, 'White')
    title_text_rect = title_text.get_rect(center=(display_width/2, 100))
    screen.blit(title_text, title_text_rect)


def display_selection():
    screen.fill((94, 129, 162))


# Code for creating window and its features
background_colour = (0, 0, 0)
(sprite_width, sprite_height) = (100, 100)  # Increase the sprite size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('DATA DASH!')

# fill the screen with a color to wipe away anything from the last frame
# screen.fill(background_colour)
state = States.INTRO

player = pygame.sprite.GroupSingle()
player.add(Player())

clock = pygame.time.Clock()
dt = 0

# initialize player position, dividing width and height by 2 will place it in the center
player_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# initialize the monster's position randomly but at least 50 spaces away from the player (this was the part)
min_distance = 50
max_distance = min(screen.get_width(), screen.get_height()) / 2 - min_distance
angle = random.uniform(0, 2 * math.pi)
distance = random.uniform(min_distance, max_distance)
monster_position = player_position + pygame.Vector2(math.cos(angle), math.sin(angle)) * distance


# Need to do this to have it display something in the first place (initialization)
current_sprite = 'sprite1'

# Timer so that the player can have a few seconds to get mentally ready before the chase
# So both the player and monster will be paused for the first 3 seconds after the program is executed
timer_duration = 3000  # 3 seconds (every 1000ms is one second)
timer_start = pygame.time.get_ticks()
timer_expired = False

# Checking continuously to see if the window is open
while True:
    for event in pygame.event.get():
        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            pygame.quit()  # pygame.quit() uninitialized everything from pygame.init()
            exit()  # ends code so pygame.display.update() does not get called, producing error

    if state == States.INTRO:
        display_intro()
    elif state == States.SELECTION:
        display_selection()
    elif state == States.ARRAYLIST:
        # this will fill the background screen with all black as initialized at the top of the program
        screen.fill(background_colour)
        player.draw(screen)
        player.update()


        # this part is the logic for the timer after the program is executed. it will check if timer_expired is True
        # if it is True then the players can/will start moving
        if not timer_expired:
            timer_elapsed = pygame.time.get_ticks() - timer_start
            if timer_elapsed >= timer_duration:
                timer_expired = True

        # this condition is the logic behind the monster. you add to the monsters position depending
        # on the player's position
        if timer_expired:
            # Adjust number getting multiplied to the dt at the end to control the speed of the monster
            monster_position += (player_position - monster_position) * dt * 1  # <- this number



    # flip() the display to put your work on the screen
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
