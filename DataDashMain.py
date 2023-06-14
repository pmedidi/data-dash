import pygame
# initialize the pygame modules
pygame.init()
# Code for creating window and its features
background_colour = (0,0,0)
(width, height) = (1000, 1000)
(sprite_width, sprite_height) = (50, 50)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('DATA DASH!')
# fill the screen with a color to wipe away anything from last frame
screen.fill(background_colour)
running = True
clock = pygame.time.Clock()
dt = 0

# initialize player position, dividing width and height by 2 will place it in the center
player_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Checking continuously to see if window is open
while running:
  for event in pygame.event.get():
    # pygame.QUIT event means the user clicked X to close your window
    if event.type == pygame.QUIT:
      running = False
  screen.fill(background_colour)

  # drawing the character hard-coded
  # pygame.Rect() syntax: the 0s are for the position of where it is spawned and
  # the last two is its width and height
  pygame.draw.rect(screen, "purple", pygame.Rect(player_position.x, player_position.y, sprite_width, sprite_height))
  #movement code

  keys = pygame.key.get_pressed()
  if keys[pygame.K_w]:
    player_position.y -= 300 * dt
  if keys[pygame.K_s]:
    player_position.y += 300 * dt
  if keys[pygame.K_a]:
    player_position.x -= 300 * dt
  if keys[pygame.K_d]:
    player_position.x += 300 * dt


  # flip() the display to put your work on screen
  pygame.display.flip()
  dt = clock.tick(60) / 1000

pygame.quit()