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
        # self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)  # The original center position/pivot point.
        # self.offset = Vector2(50, 0)  # We shift the sprite 50 px to the right.
        self.walkingspeed = 5
        self.heading = 0
        self.scale = .3
        self.is_player = False
        self.world = None
        self.id = id(self)

    def __repr__(self) -> str:
        return super().__repr__() + f" at {self.pos[0]}, {self.pos[1]}\n"

    def render(self, camera_pos, screen_center, zoom_level):
        # Render the sprite with the camera offset.
        # camera_pos = screen_center
        surface = self.world.surface
        size = surface.get_size()
        tile_width = size[0] / zoom_level
        if self.is_player:
            self.image = pg.transform.scale(self.orig_image, [tile_width, tile_width * 3.459]) # fixed aspect ratio (512/148)
            self.blit_x = screen_center[0] - self.image.get_width() // 2
            self.blit_y = screen_center[1] - self.image.get_height() // 2
            # print(f"{screen_center[0]} - {self.image.get_width() // 2} = {self.blit_x}")
            # print(f"player at {self.blit_x}, {self.blit_y}")
        else:
            self.image = pg.transform.scale(self.orig_image, [tile_width, tile_width]) # fixed aspect ratio (512/148)
            self.blit_x = (self.pos[0] - camera_pos[0]) * tile_width #- self.image.get_width() // 2
            self.blit_y = size[1] - (self.pos[1] - camera_pos[1]) * tile_width #- self.image.get_height() // 2
            # print(f"{self.pos[0]} / {zoom_level} - {camera_pos[0]} - {self.image.get_width() // 2} = {self.blit_x}")
            # print(f"tile at {self.blit_x}, {self.blit_y}")

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
        self.image = self.spritesheet.subsurface((0, 0, 148, 512))
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
        print(self.pos)

        if heading == 0:
            # ...#
            # ....
            ###print("heading 0", self.spritesheet.get_size())
            self.orig_image = self.spritesheet.subsurface((256*3, 0, 148, 512))
        elif heading == 45:
            # .#..
            # ....
            ###print("heading 45")
            self.orig_image = self.spritesheet.subsurface((256*2, 512, 148, 512))
        elif heading == 90:
            # #...
            # ....
            ###print("heading 90")
            self.orig_image = self.spritesheet.subsurface((0, 512, 148, 512))
        elif heading == 135:
            # ..#.
            # ....
            ###print("heading 135")
            self.orig_image = self.spritesheet.subsurface((256, 512, 148, 512))
        elif heading == 180:
            # ....
            # ...#
            ###print("heading 180")
            self.orig_image = self.spritesheet.subsurface((256*3, 512, 148, 512))
        elif heading == -135:
            # ....
            # .#..
            ###print("heading -135")
            self.orig_image = self.spritesheet.subsurface((256*2, 0, 148, 512))
        elif heading == -90:
            # ....
            # #...
            ###print("heading -90")
            self.orig_image = self.spritesheet.subsurface((0, 0, 148, 512))
        elif heading == -45:
            # ....
            # ..#.
            ###print("heading -45")
            self.orig_image = self.spritesheet.subsurface((256, 0, 148, 512))

class Tile(Entity):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pg.image.load("sand.jpg")
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.is_player = False