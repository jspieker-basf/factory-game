import pygame
import random
pygame.init()

# Set up the screen
# size = (700, 500)
size = (1920, 1080)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("DVD Simulator")

# Set up the colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pink = (255, 200, 200)
magenta = (255, 0, 255)
cyan = (0, 255, 255)
yellow = (255, 255, 0)
orange = (255, 165, 0)
purple = (128, 0, 128)
colors = [red, green, blue, pink, magenta, cyan, yellow, orange, purple]

# Set up the game loop
done = False

# Set up the clock
clock = pygame.time.Clock()

# Main loop 

xpos = random.randint(0, int(size[0]/2))
ypos = random.randint(0, int(size[1]/2))
ydir = 1
xdir = 1
increment = 5

def change_color():
    r_col = random.choice(colors)
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    image.fill(r_col[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

image = pygame.image.load("dvd.svg")
# Load the image
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(white)

    # Scale the image to the desired size
    image = pygame.transform.scale(image, (74*5, 34*5))

    # Draw the image on the screen
    screen.blit(image, (xpos, ypos))
    pygame.display.flip()
    if ydir == 1:
        ypos += increment
        if ypos > size[1] - image.get_height():
            change_color()
            ydir = 0
    else:
        ypos -= increment
        if ypos < 0:
            change_color()
            ydir = 1
    if xdir == 1:
        xpos += increment
        if xpos > size[0] - image.get_width():
            change_color()
            xdir = 0
    else:
        xpos -= increment
        if xpos < 0:
            change_color()
            xdir = 1


    clock.tick(60)