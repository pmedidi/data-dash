import pygame
import random
import math

# initialize the game
pygame.init()

# Code for creating window and its features
background_colour = (0, 0, 0)
(width, height) = (1000, 1000)
(sprite_width, sprite_height) = (100, 100)  # Increase the sprite size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('DATA DASH!')

# fill the screen with a color to wipe away anything from the last frame
screen.fill(background_colour)

running = True
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

# initialize my sprites images to variables
sprite_images = {
    'sprite1': pygame.image.load('RightCat.png'),
    'sprite2': pygame.image.load('LeftCat.png'),
    'sprite3': pygame.image.load('DownCat.png'),
    'sprite4': pygame.image.load('UpCat.png')
}

# Need to do this to have it display something in the first place (initialization)
current_sprite = 'sprite1'

# Timer so that the player can have a few seconds to get mentally ready before the chase
# So both the player and monster will be paused for the first 3 seconds after the program is executed
timer_duration = 3000  # 3 seconds (every 1000ms is one second)
timer_start = pygame.time.get_ticks()
timer_expired = False

# Checking continuously to see if the window is open
while running:
    for event in pygame.event.get():
        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

    # this will fill the background screen with all black as initialized at the top of the program
    screen.fill(background_colour)

    # blit() puts the image on the screen. you can also customize the sprite width and height as well as its position
    # on the screen
    screen.blit(pygame.transform.scale(sprite_images[current_sprite], (sprite_width, sprite_height)), player_position)

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

    # This part is for the monster to be displayed on the screen (customized size and position)
    screen.blit(pygame.transform.scale(sprite_images[current_sprite], (sprite_width, sprite_height)),
                monster_position)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        current_sprite = 'sprite4'
        if player_position.y > 0:
            player_position.y -= 300 * dt
            if player_position.y < 50:
                player_position.y = 50
    if keys[pygame.K_DOWN]:
        current_sprite = 'sprite3'
        if player_position.y < height - sprite_height - 100:
            player_position.y += 300 * dt
            if player_position.y > height - sprite_height - 100:
                player_position.y = height - sprite_height - 100
    if keys[pygame.K_LEFT]:
        current_sprite = 'sprite2'
        if player_position.x > 0:
            player_position.x -= 300 * dt
            if player_position.x < 0:
                player_position.x = 0
    if keys[pygame.K_RIGHT]:
        current_sprite = 'sprite1'
        if player_position.x < width - sprite_width:
            player_position.x += 300 * dt
            if player_position.x > width - sprite_width:
                player_position.x = width - sprite_width

    # flip() the display to put your work on the screen
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
