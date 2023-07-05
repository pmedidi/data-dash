import pygame
import random
import math
from sys import exit
from enum import Enum

# global variables
# 2d array of buttons for each level/State
buttons = []

# screen and border numbers
display_height = 600
display_width = display_height + 100
border = 10
(width, height) = (display_width, display_height)


class States(Enum):
    INTRO = 0
    SELECTION = 1
    ARRAYLIST = 2


# Player class used to make the cat/player and currently only handles player input and updates location
class Player(pygame.sprite.Sprite):
    def __init__(self):  # constructor
        super().__init__()
        # sprite images and scaling
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

    # reads user input and updates the cat's position and image accordingly
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

    # updates player
    def update(self):
        self.player_input()


# Button class used to create buttons for the game
# button_state -> State enum that the button belongs in
# onePress -> I THINK true means it runs for as long as its held down
class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, button_state=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        # if one press is true -> as long as you hold it down, the button will call the function
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'default': '#f5f5f5',
            'hover': '#e8e8e8',
            'clicked': '#d1d1d1',
        }
        self.button_surface = pygame.Surface((self.width, self.height))
        # self.height = self.button_surface.get_height()
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.button_text = button_font.render(buttonText, False, 'Black')
        buttons[button_state.value].append(self)

    # checks to see if the mouse 'collides' with the button
    def process(self):
        mouse_position = pygame.mouse.get_pos()
        self.button_surface.fill(self.fillColors['default'])
        if self.button_rect.collidepoint(mouse_position):
            self.button_surface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.fillColors['clicked'])
                if self.onePress:  # i have no idea what onePress and alreadyPress does but is ok
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        # blit text onto surface
        self.button_surface.blit(self.button_text, [
            self.button_rect.width/2 - self.button_text.get_rect().width/2,
            self.button_rect.height/2 - self.button_text.get_rect().height/2
        ])
        # blit surface onto screen
        screen.blit(self.button_surface, self.button_rect)


# uses buttons array and creates an array for each state inside the buttons array
# each array in buttons[] represents the buttons in each state/level/page
def create_button_array():
    global buttons
    for state in States:
        buttons.append([])


# processes every button in the button list passed through
def process_buttons(buttons):
    for button in buttons:
        button.process()


# function to display the intro screen
def display_intro():
    screen.fill((178, 190, 181))  # off gray color
    title_text = title_font.render('Data Dash', False, 'White')
    title_text_rect = title_text.get_rect(center=(display_width / 2, 100))
    screen.blit(title_text, title_text_rect)

    if not buttons[States.INTRO.value]:
        button_width = 500
        x_button_pos = (display_width / 2) - (button_width / 2)
        buttons[States.INTRO.value].append(Button(int(x_button_pos), 200, button_width, 70, 'Continue',
                                                  to_arraylist, States.INTRO))
        buttons[States.INTRO.value].append(Button(int(x_button_pos), 300, button_width, 70, 'Level Select',
                                                  to_arraylist, States.INTRO))
        buttons[States.INTRO.value].append(Button(int(x_button_pos), 400, button_width, 70, 'Exit', exit, States.INTRO))

    process_buttons(buttons[States.INTRO.value])


# function to display the selection screen
def display_selection():
    screen.fill((94, 129, 162))


# function that reassigns state to arraylist state
def to_arraylist():
    global state
    state = States.ARRAYLIST


# initialize the game
pygame.init()
create_button_array()



state = States.INTRO

# fonts
title_font = pygame.font.Font('font/Pixeltype.ttf', 100)
button_font = pygame.font.Font('font/Pixeltype.ttf', 64)

# Code for creating window and its features
background_colour = (0, 0, 0)
(sprite_width, sprite_height) = (100, 100)  # Increase the sprite size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('DATA DASH!')


# player intialization
player = pygame.sprite.GroupSingle()
player.add(Player())

# initialize player position, dividing width and height by 2 will place it in the center
player_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# clock
clock = pygame.time.Clock()
dt = 0

# initialize the monster's position randomly but at least 50 spaces away from the player (this was the part)
min_distance = 50
max_distance = min(screen.get_width(), screen.get_height()) / 2 - min_distance
angle = random.uniform(0, 2 * math.pi)
distance = random.uniform(min_distance, max_distance)
monster_position = player_position + pygame.Vector2(math.cos(angle), math.sin(angle)) * distance


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

    # determines state
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
    dt = clock.tick(60) / 1000.0
