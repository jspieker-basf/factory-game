import pygame

class Engineer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("engineer.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def move(self, direction: tuple[int, int]):
        self.rect.x += direction[0]
        self.rect.y += direction[1] 
        print(f"Engineer moved {direction}")