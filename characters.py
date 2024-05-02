import pygame as pg
from pygame.math import Vector2

class Entity(pg.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((122, 70), pg.SRCALPHA)
        pg.draw.polygon(self.image, pg.Color('dodgerblue1'),
                        ((1, 0), (120, 35), (1, 70)))
        # A reference to the original image to preserve the quality.
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)  # The original center position/pivot point.
        self.offset = Vector2(50, 0)  # We shift the sprite 50 px to the right.
        self.walkingspeed = 2
        self.heading = 0
        self.scale = 0.6

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pg.transform.rotozoom(self.orig_image, -self.heading, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.heading)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.pos+offset_rotated)

class Engineer(Entity):
    def __init__(self, pos):
        super().__init__(pos)
        self.spritesheet = pg.image.load("engineer_spritesheet.tga")
        self.image = self.spritesheet.subsurface((0, 0, 256, 512))
        self.image = pg.transform.scale(self.image, [x * self.scale for x in self.image.get_size()])
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=(128, 256))


    def move(self, direction: tuple[int, int], heading: int):
        
        self.pos.x += direction[0] * self.walkingspeed
        self.pos.y += direction[1] * self.walkingspeed
        self.rect.center = self.pos
        self.prev_heading = self.heading
        self.heading = heading

        if heading == 0:
            self.image = self.spritesheet.subsurface((256*3, 0, 256, 512))
        elif heading == 45:
            self.image = self.spritesheet.subsurface((256, 0, 256, 512))
        elif heading == 90:
            self.image = self.spritesheet.subsurface((0, 0, 256, 512))
        elif heading == 135:
            self.image = self.spritesheet.subsurface((256*2, 0, 256, 512))
        elif heading == 180:
            self.image = self.spritesheet.subsurface((256*3, 512, 256, 512))
        elif heading == -135:
            self.image = self.spritesheet.subsurface((256, 512, 256, 512))
        elif heading == -90:
            self.image = self.spritesheet.subsurface((0, 512, 256, 512))
        elif heading == -45:
            self.image = self.spritesheet.subsurface((256*2, 512, 256, 512))
        
        self.image = pg.transform.scale(self.image, [x * self.scale for x in self.image.get_size()])
        # self.rotate() if self.heading != self.prev_heading else None
        print(f"Engineer moved {self.heading}° ({direction}), now at ({self.rect.x}, {self.rect.y})")