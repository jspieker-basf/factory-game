import pygame as pg
from entities import *
from world import World
import math
# Initialize Pygame
pg.init()

# Set up the game window
window_width = 960
window_height = 540
window = pg.display.set_mode((window_width, window_height))
pg.display.set_caption("Factory Game")
# setup world
world = World("Nauvis", window)
eng = Engineer((0,0))
tiles = []
for x in range(0,2):
    for y in range(0, 2):
        world.add_entity(Tile((x,y)))

world.add_entity(eng)

print(world.entities)

clock = pg.time.Clock()

# Game loop
running = True
while running:
    window.fill((0, 0, 0))
    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEWHEEL:
            # eng.walkingspeed += event.y
            world.zoom(-event.y)
        if event.type == pg.K_SPACE:
            # eng.rotate()
            pass
    keystate = pg.key.get_pressed()
    if keystate[pg.K_LEFT] and keystate[pg.K_RIGHT] and keystate[pg.K_UP] and keystate[pg.K_DOWN]:
        dir = (0, 0)
    elif keystate[pg.K_LEFT] and keystate[pg.K_UP]:
        dir = (-1, 1)
    elif keystate[pg.K_LEFT] and keystate[pg.K_DOWN]:
        dir = (-1, -1)
    elif keystate[pg.K_RIGHT] and keystate[pg.K_UP]:
        dir = (1, 1)
    elif keystate[pg.K_RIGHT] and keystate[pg.K_DOWN]:
        dir = (1, -1)
    elif keystate[pg.K_LEFT] and keystate[pg.K_RIGHT]:
        dir = (0, 0)
    elif keystate[pg.K_UP] and keystate[pg.K_DOWN]:
        dir = (0, 0)
    elif keystate[pg.K_LEFT]:
        dir = (-1, 0)
    elif keystate[pg.K_RIGHT]:
        dir = (1, 0)
    elif keystate[pg.K_UP]:
        dir = (0, 1)
    elif keystate[pg.K_DOWN]:
        dir = (0, -1)
    else:
        dir = (0, 0)
    if dir != (0, 0):
        heading = math.degrees(math.atan2(dir[1], dir[0]))
        eng.move(dir, heading)

    # Render graphics
    # Fill the window with a tilable texture
    # texture = pg.image.load("sand.jpg")
    # texture_width = texture.get_width()
    # texture_height = texture.get_height()
    # for x in range(0, window_width, texture_width):
    #     for y in range(0, window_height, texture_height):
    #         window.blit(texture, (x, y))

    # Render the world
    # world.entities[0].render(window, world.relative_position, world.screen_center, (window_width/world.zoom_level, window_height/world.zoom_level))

    # Update the display
    clock.tick(60)
    world.render()
    pg.display.flip()

# Quit the game
pg.quit()