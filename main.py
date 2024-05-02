import pygame as pg
from characters import Entity, Engineer
import pygame.examples.aliens
import math
# Initialize Pygame
pg.init()

# Set up the game window
window_width = 800
window_height = 600
window = pg.display.set_mode((window_width, window_height))
pg.display.set_caption("Factory Game")

# setup
eng = Engineer((50,50))
clock = pg.time.Clock() 

# Game loop
running = True
while running:
    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            eng.walkingspeed += event.y
        if event.type == pygame.KSCAN_SPACE:
            eng.rotate()
    keystate = pg.key.get_pressed()
    if keystate[pg.K_LEFT] and keystate[pg.K_UP]:
        dir = (-1, -1)
    elif keystate[pg.K_LEFT] and keystate[pg.K_DOWN]:
        dir = (-1, 1)
    elif keystate[pg.K_RIGHT] and keystate[pg.K_UP]:
        dir = (1, -1)
    elif keystate[pg.K_RIGHT] and keystate[pg.K_DOWN]:
        dir = (1, 1)
    elif keystate[pg.K_LEFT] and keystate[pg.K_RIGHT]:
        dir = (0, 0)
    elif keystate[pg.K_UP] and keystate[pg.K_DOWN]:
        dir = (0, 0)
    elif keystate[pg.K_LEFT]:
        dir = (-1, 0)
    elif keystate[pg.K_RIGHT]:
        dir = (1, 0)
    elif keystate[pg.K_UP]:
        dir = (0, -1)
    elif keystate[pg.K_DOWN]:
        dir = (0, 1)
    else:
        dir = (0, 0)
    if dir != (0, 0):
        heading = math.degrees(math.atan2(dir[1], dir[0]))
        eng.move(dir, heading)

    # Render graphics
    # Fill the window with a tilable texture
    texture = pg.image.load("sand.jpg")
    texture_width = texture.get_width()
    texture_height = texture.get_height()
    for x in range(0, window_width, texture_width):
        for y in range(0, window_height, texture_height):
            window.blit(texture, (x, y))

    # Update the display
    window.blit(eng.image, eng.rect)
    clock.tick(60)
    pg.display.flip()

# Quit the game
pg.quit()