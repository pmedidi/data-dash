import pygame

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

# Load and resize the sprite images
sprite_images = {
    'sprite1': pygame.image.load('RightCat.png'),
    'sprite2': pygame.image.load('LeftCat.png'),
    'sprite3': pygame.image.load('DownCat.png'),
    'sprite4': pygame.image.load('UpCat.png')
}

# Need to do this to have it display something in the first place (initialization)
current_sprite = 'sprite1'

# Checking continuously to see if the window is open
while running:
    for event in pygame.event.get():
        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_colour)

    screen.blit(pygame.transform.scale(sprite_images[current_sprite], (sprite_width, sprite_height)), player_position)

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
