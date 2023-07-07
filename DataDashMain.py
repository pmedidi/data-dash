import pygame
from random import randint
from sys import exit
from enum import Enum

# global variables
# 2d array of buttons for each level/State
buttons = []
obstacles = []

# screen and border numbers
display_height = 600
display_width = display_height + 300
border = 10
(width, height) = (display_width, display_height)
default_obstacle_size = (55, 55)
obstacle_border = default_obstacle_size[0]
num_columns = (display_width - (border * 2)) / default_obstacle_size[0]
num_rows = (display_height - (border * 2)) / default_obstacle_size[0]


class States(Enum):
    INTRO = 0
    SELECTION = 1
    ARRAYLIST = 2


class Directions(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Obstacles(Enum):
    ROCK = 0
    BOX = 1


# Player class used to make the cat/player and currently only handles player input and updates location
class Player(pygame.sprite.Sprite):
    def __init__(self):  # constructor
        super().__init__()
        # sprite images and scaling
        right_cat = pygame.image.load('images/player/RightCat.png').convert_alpha()
        right_cat = pygame.transform.scale(right_cat, default_obstacle_size)
        left_cat = pygame.image.load('images/player/LeftCat.png').convert_alpha()
        left_cat = pygame.transform.scale(left_cat, default_obstacle_size)
        down_cat = pygame.image.load('images/player/DownCat.png').convert_alpha()
        down_cat = pygame.transform.scale(down_cat, default_obstacle_size)
        up_cat = pygame.image.load('images/player/UpCat.png').convert_alpha()
        up_cat = pygame.transform.scale(up_cat, default_obstacle_size)

        self.sprite_directions = [right_cat, left_cat, down_cat, up_cat]
        self.sprite_index = 0
        self.speed = 300

        self.image = self.sprite_directions[self.sprite_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))

    # reads user input and updates the cat's position and image accordingly
    def player_input(self):
        keys = pygame.key.get_pressed()
        displacement = self.speed * dt      # distance player will move
        if keys[pygame.K_UP]:
            self.sprite_index = 3
            if (self.rect.top - displacement) < border:
                self.rect.top = border
            elif not self.collision(obstacles[state.value], Directions.UP, displacement):
                self.rect.y -= displacement
        elif keys[pygame.K_DOWN]:
            self.sprite_index = 2
            if (self.rect.bottom + displacement) > height - border:
                self.rect.bottom = height - border
            elif not self.collision(obstacles[state.value], Directions.DOWN, displacement):
                self.rect.y += displacement
        elif keys[pygame.K_LEFT]:
            self.sprite_index = 1
            if (self.rect.left - displacement) < border:
                self.rect.left = border
            elif not self.collision(obstacles[state.value], Directions.LEFT, displacement):
                self.rect.x -= displacement
        elif keys[pygame.K_RIGHT]:
            self.sprite_index = 0
            if (self.rect.right + displacement) > width - border:
                self.rect.right = width - border
            elif not self.collision(obstacles[state.value], Directions.RIGHT, displacement):
                self.rect.x += displacement
        if keys[pygame.K_SPACE]:
            self.closest_crate(obstacles[state.value])
        # updates cat image
        self.image = self.sprite_directions[self.sprite_index]

    def collision(self, obstacles, direction, displacement):
        player_rect = self.rect
        for obstacle in obstacles:
            obst_rect = obstacle.rect
            if obst_rect.left < player_rect.right < obst_rect.right \
                    or obst_rect.left < player_rect.left < obst_rect.right or obst_rect.centerx == player_rect.centerx:
                if direction == Directions.UP:
                    y_pos = player_rect.top - displacement
                    if obst_rect.top < y_pos < obst_rect.bottom:
                        player_rect.top = obst_rect.bottom
                        return True
                elif direction == Directions.DOWN:
                    y_pos = player_rect.bottom + displacement
                    if obst_rect.bottom > y_pos > obst_rect.top:
                        player_rect.bottom = obst_rect.top
                        return True
            elif obst_rect.top < player_rect.top < obst_rect.bottom \
                    or obst_rect.top < player_rect.bottom < obst_rect.bottom or obst_rect.centery == player_rect.centery:
                if direction == Directions.RIGHT:
                    x_pos = player_rect.right + displacement
                    if obst_rect.left < x_pos < obst_rect.right:
                        player_rect.right = obst_rect.left
                        return True
                elif direction == Directions.LEFT:
                    x_pos = player_rect.left - displacement
                    if obst_rect.right > x_pos > obst_rect.left:
                        player_rect.left = obst_rect.right
                        return True
        return False

    def closest_crate(self, obstacles):
        box_obstacles = filter(lambda o: o.obstacle_type == Obstacles.BOX, obstacles)
        nearest_box = None

        for box in box_obstacles:
            if box.rect.left < self.rect.centerx < box.rect.right:
                if box.rect.top == self.rect.bottom or box.rect.bottom == self.rect.top:
                    nearest_box = box
            elif box.rect.top < self.rect.centery < box.rect.bottom:
                if box.rect.left == self.rect.right or box.rect.right == self.rect.left:
                    nearest_box = box

        if nearest_box:
            print(nearest_box.number)
        else:
            print("NONE")


    # updates player
    def update(self):
        self.player_input()


# Button class used to create buttons for the game
# button_state -> State enum that the button belongs in
# onePress -> I THINK true means it runs for as long as its held down
class Button:
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, button_state=None,
                 onePress=False):
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
            self.button_rect.width / 2 - self.button_text.get_rect().width / 2,
            self.button_rect.height / 2 - self.button_text.get_rect().height / 2
        ])
        # blit surface onto screen
        screen.blit(self.button_surface, self.button_rect)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, scale=False, obstacle_type=Obstacles.ROCK, obstacle_state=None, number=None):
        super().__init__()
        self.x = x
        self.y = y
        self.scale = scale
        self.img = pygame.image.load('images/rock.png').convert_alpha()
        self.number = number
        self.obstacle_type = obstacle_type
        self.obstacle_state = obstacle_state

        if obstacle_type == Obstacles.ROCK:
            if randint(0, 1):
                self.img = pygame.transform.flip(self.img, True, False)
        if obstacle_type == Obstacles.BOX:
            self.img = pygame.image.load('images/crates/crate.png').convert_alpha()
            self.img = pygame.transform.scale(self.img, default_obstacle_size)
            if number is not None:
                num_img = pygame.image.load('images/crates/three.png').convert_alpha()
                if number == 4:
                    num_img = pygame.image.load('images/crates/four.png').convert_alpha()
                num_img = pygame.transform.scale(num_img, default_obstacle_size)
                img_surface = pygame.Surface(default_obstacle_size)
                img_surface.blit(self.img, (0, 0))
                img_surface.blit(num_img, (0, 0))
                self.img = img_surface

        if scale:
            self.img = pygame.transform.scale(self.img, (110, 110))
        else:
            self.img = pygame.transform.scale(self.img, default_obstacle_size)

        self.rect = self.img.get_rect(topleft=(self.x, self.y))
        obstacles[obstacle_state.value].append(self)

    def process(self):
        # blit surface onto screen
        screen.blit(self.img, self.rect)


# uses buttons array and creates an array for each state inside the buttons array
# each array in buttons[] represents the buttons in each state/level/page
def create_button_and_obst_array():
    global buttons
    global obstacles

    for state in States:
        buttons.append([])
        obstacles.append([])


# processes every button in the button list passed through
def display_buttons(buttons):
    for button in buttons:
        button.process()


def display_obstacles(obstacles):
    for rock in obstacles:
        rock.process()


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

    display_buttons(buttons[States.INTRO.value])


# function to display the selection screen
def display_selection():
    screen.fill((94, 129, 162))


def display_arraylist(player):
    # this will fill the background screen with all black as initialized at the top of the program
    screen.fill((24, 133, 67))
    player.draw(screen)
    player.update()

    if not obstacles[States.ARRAYLIST.value]:
        rock1 = Obstacle(65, 100, False, Obstacles.ROCK, States.ARRAYLIST)
        rock2 = Obstacle(175, 155, True, Obstacles.ROCK, States.ARRAYLIST)
        crate1 = Obstacle(285, 265, False, Obstacles.BOX, States.ARRAYLIST, 3)
        crate1 = Obstacle(340, 265, False, Obstacles.BOX, States.ARRAYLIST, 4)
        crate1 = Obstacle(395, 265, False, Obstacles.BOX, States.ARRAYLIST)
    display_obstacles(obstacles[States.ARRAYLIST.value])


# function that reassigns state to arraylist state
def to_arraylist():
    global state
    state = States.ARRAYLIST


# initialize the game
pygame.init()
create_button_and_obst_array()

state = States.INTRO

# fonts
title_font = pygame.font.Font('font/Pixeltype.ttf', 100)
button_font = pygame.font.Font('font/Pixeltype.ttf', 64)

# Code for creating window and its features
background_colour = (0, 0, 0)
(sprite_width, sprite_height) = (100, 100)  # Increase the sprite size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('DATA DASH!')

# player initialization
player = pygame.sprite.GroupSingle()
player.add(Player())

# initialize player position, dividing width and height by 2 will place it in the center
player_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# clock
clock = pygame.time.Clock()
dt = 0

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
        elif event.type == pygame.KEYDOWN and state == States.ARRAYLIST:
            if event.key == pygame.K_ESCAPE:
                state = States.INTRO

    # determines state
    if state == States.INTRO:
        display_intro()
    elif state == States.SELECTION:
        display_selection()
    elif state == States.ARRAYLIST:
        display_arraylist(player)

    # flip() the display to put your work on the screen
    pygame.display.flip()
    dt = clock.tick(60) / 1000.0
