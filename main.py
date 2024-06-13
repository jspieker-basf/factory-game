import pygame as pg
from entities import *
from world import World
import math

# Constants
TICKRATE = 60

# Initialize Pygame
pg.init()
font = pg.font.SysFont("Comic Sans MS", 25)

# Set up the game window
# window_width = 960
# window_height = 540
window_width = 1920
window_height = 1080
window = pg.display.set_mode((window_width, window_height))
pg.display.set_caption("Factory Game")

# Set up the clock
time = pg.time
clock = time.Clock()

# Set up world
world = World("Nauvis", window, time, font)

tiles = [Tile(x, y) for x in range(-10,10) for y in range(-10, 10)]
world.add_entities(tiles)

copper_ores = [CopperOre(0, 2, 150), CopperOre(1, 2, 300), CopperOre(1, 3, 250)]
iron_ores = [IronOre(5, -3, 200), IronOre(-3, 3, 200), IronOre(-3, 2, 200)]
coal = [Coal(6, 4, 200), Coal(7, 4, 200), Coal(7, 5, 200), Coal(5, 4, 200)]
world.add_entities(copper_ores)
world.add_entities(iron_ores)
world.add_entities(coal)

trees = [Tree(3, 2), Tree(-6, 0)]
world.add_entities(trees)

oven = Oven(-2, 4)
eng = Engineer(0, 0)
world.add_entities([oven, eng])

# def read_mousebutton_state():
#     left, middle, right = pg.mouse.get_pressed()
#     return left, middle, right

# Game loop
running = True
while running:
    window.fill((100,100,100))
    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_status = pg.mouse.get_pressed()
            pos = pg.mouse.get_pos()
            # get list of sprites that are under the mouse cursor
            clicked_sprites = [s for s in world.entities if s.rect.collidepoint(pos)]
            world.cursor(clicked_sprites, mouse_status)
        if event.type == pg.KEYDOWN and event.key == pg.K_F1:
            world.toggle_grid()
    eng.move()
    # print(read_mousebutton_state())
    # Update the display
    clock.tick(TICKRATE)
    world.render()
    pg.display.flip()

# Done! Time to quit.
pg.quit()
