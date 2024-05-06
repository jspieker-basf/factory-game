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
        self.scale = 1
        self.is_player = False
        self.world = None

    def __repr__(self) -> str:
        return super().__repr__() + f" at {self.pos[0]}, {self.pos[1]}\n"

    def render(self, surface, camera_pos, screen_center, zoom_level):
        # Render the sprite with the camera offset.
        # camera_pos = screen_center
        self.image = pg.transform.scale(self.orig_image, [self.orig_image.get_width() * 1 / zoom_level, self.orig_image.get_height() * 1 / zoom_level])

        self.blit_x

        self.rect = self.image.get_rect(center=(self.blit_x, self.blit_y))

        surface.blit(self.image, (self.blit_x, self.blit_y))
        if self.__repr__().startswith("<Tile"):
            # ###print(f"etzadla wird {self} gerendert bei {self.blit_x}, {self.blit_y}")
            pass
        pass

class Engineer(Entity):
    def __init__(self, pos):
        super().__init__(pos)
        self.spritesheet = pg.image.load("engineer_spritesheet.tga")
        self.image = self.spritesheet.subsurface((0, 0, 256, 512))
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=(self.image.get_width()//2, self.image.get_height() // 2))
        self.is_player = True


    def move(self, direction: tuple[int, int], heading: int):

        self.pos.x += direction[0] * self.walkingspeed / 10 * (0.7071 if direction[0] and direction[1] != 0 else 1) # 0.707 is the sin/cos of 45°
        self.pos.y += direction[1] * self.walkingspeed / 10 * (0.7071 if direction[0] and direction[1] != 0 else 1) # 0.707 is the sin/cos of 45°
        self.rect.center = self.pos
        self.prev_heading = self.heading
        self.heading = heading

        #set relative position to players position
        self.world.setRelativePosition(self.pos)

        ###print(f'headed {heading}°, moving {direction}')

        if heading == 0:
            # ...#
            # ....
            ###print("heading 0", self.spritesheet.get_size())
            self.image = self.spritesheet.subsurface((256*3, 0, 256, 512))
        elif heading == 45:
            # .#..
            # ....
            ###print("heading 45")
            self.image = self.spritesheet.subsurface((256, 0, 256, 512))
        elif heading == 90:
            # #...
            # ....
            ###print("heading 90")
            self.image = self.spritesheet.subsurface((0, 0, 256, 512))
        elif heading == 135:
            # ..#.
            # ....
            ###print("heading 135")
            self.image = self.spritesheet.subsurface((256*2, 0, 256, 512))
        elif heading == 180:
            # ....
            # ...#
            ###print("heading 180")
            self.image = self.spritesheet.subsurface((256*3, 512, 256, 512))
        elif heading == -135:
            # ....
            # .#..
            ###print("heading -135")
            self.image = self.spritesheet.subsurface((256, 512, 256, 512))
        elif heading == -90:
            # ....
            # #...
            ###print("heading -90")
            self.image = self.spritesheet.subsurface((0, 512, 256, 512))
        elif heading == -45:
            # ....
            # ..#.
            ###print("heading -45")
            self.image = self.spritesheet.subsurface((256*2, 512, 256, 512))

        image_size = self.image.get_size()
        self.image = pg.transform.scale(self.image, (image_size[0] * self.scale, image_size[1] * self.scale))
        # self.rotate() if self.heading != self.prev_heading else None
        # ###print(f"Engineer moved {self.heading}° {direction}, now at ({self.pos.x}, {self.pos.y})")

class Tile(Entity):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pg.image.load("sand.jpg")
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.is_player = False