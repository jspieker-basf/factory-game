import pygame
from characters import Engineer
import pygame.examples.aliens
# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Factory Game")

# setup
eng = Engineer()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            eng.move((1, 1))
        if event.type == pygame.K_RIGHT and event.key == pygame.KEYDOWN:
            eng.move((1, -1))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            eng.move((-1, -1))
        if event.type == pygame.K_LEFT and event.key == pygame.KEYUP:
            eng.move((-1, 1))
        if event.type == pygame.KEYDOWN:
            eng.move((0, -1))
        if event.type == pygame.KEYUP:
            eng.move((0, 1))
        if event.type == pygame.K_LEFT:
            eng.move((-1, 0))
        if event.type == pygame.K_RIGHT:
            eng.move((1, 0))
        window.blit(eng.image, eng.rect)

    # Render graphics
    window.fill((0, 0, 0))  # Fill the window with black color

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()