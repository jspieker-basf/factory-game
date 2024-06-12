import pygame as pg
import math

class Message():
    def __init__(self, content, expiration):
        self.content = content
        self.expiration = expiration

class Entity(pg.sprite.Sprite):
    def __init__(self, posX, posY):
        super().__init__()
        self.posX = posX
        self.posY = posY
        self.world = None
        self.id = id(self)
        self.image = None
        self.messages = []

    def __repr__(self) -> str:
        return super().__repr__() + f" ID: {self.id} at {self.posX}, {self.posY}"
    
    def set_message(self, message):
        self.messages.insert(0, Message(message, self.world.time.get_ticks() + 2500))

    def render_messages(self):
        c_time = self.world.time.get_ticks()
        offset = 1
        self.messages = [message for message in self.messages if c_time < message.expiration]
        for message in self.messages:
            self.world.surface.blit(self.world.font.render(message.content, True, pg.Color('white')), (self.rect.left + 50 + 25 * offset, self.rect.top + 25 * -offset))
            offset += 1

    def render(self):
        if self.world is None:
            raise Exception("Entity is not in a world")
        elif self.image is None:
            raise Exception("Entity has no image")
        else:
            if self.is_player:
                self.image = pg.transform.scale(self.image, [self.world.tile_size, self.world.tile_size * 3.459]) # fixed aspect ratio (512/148)
            else:
                self.image = pg.transform.scale(self.image, [self.world.tile_size, self.world.tile_size])
            centerX = self.world.surface.get_width() // 2
            centerY = self.world.surface.get_height() // 2
            blitX = centerX + self.posX * self.world.tile_size
            blitY = centerY - self.posY * self.world.tile_size 
            self.world.surface.blit(self.image, (blitX, blitY))
            self.render_messages() if self.messages else None
            self.rect = self.image.get_rect(top=blitY, left=blitX)
            # print(self.rect, self.__repr__())
            # print(self.ret)

class Engineer(Entity):
    def __init__(self, posX, posY):
        super().__init__(posX, posY)
        self.spritesheet = pg.image.load("../factory-game/engineer_spritesheet.tga")
        self.update_rotation(-90)
        # self.rect = self.image.get_rect(center=(self.image.get_width()//2, self.image.get_height() // 2))
        self.is_player = True
        self.inventory = []

    def move(self):
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
            velocity = 2.5 / 60  # 5 tiles/second at 60 ticks
            delta_x = velocity * math.cos(math.radians(heading))
            delta_y = velocity * math.sin(math.radians(heading))
            self.posX += delta_x
            self.posY += delta_y
            # print(self.posX, self.posY)
            self.update_rotation(heading)

    def update_rotation(self, heading):
        if heading == 0:
            # ...#
            # ....
            ###print("heading 0", self.spritesheet.get_size())
            self.image = self.spritesheet.subsurface((256*3, 0, 148, 512))
        elif heading == 45:
            # .#..
            # ....
            ###print("heading 45")
            self.image = self.spritesheet.subsurface((256*2, 512, 148, 512))
        elif heading == 90:
            # #...
            # ....
            ###print("heading 90")
            self.image = self.spritesheet.subsurface((0, 512, 148, 512))
        elif heading == 135:
            # ..#.
            # ....
            ###print("heading 135")
            self.image = self.spritesheet.subsurface((256, 512, 148, 512))
        elif heading == 180:
            # ....
            # ...#
            ###print("heading 180")
            self.image = self.spritesheet.subsurface((256*3, 512, 148, 512))
        elif heading == -135:
            # ....
            # .#..
            ###print("heading -135")
            self.image = self.spritesheet.subsurface((256*2, 0, 148, 512))
        elif heading == -90:
            # ....
            # #...
            ###print("heading -90")
            self.image = self.spritesheet.subsurface((0, 0, 148, 512))
        elif heading == -45:
            # ....
            # ..#.
            ###print("heading -45")
            self.image = self.spritesheet.subsurface((256, 0, 148, 512))

class Tile(Entity):
    def __init__(self, posX, posY):
        super().__init__(posX, posY)
        self.image = pg.image.load("../factory-game/sand.jpg")
        self.is_player = False

class Ore(Entity):
    def __init__(self, posX, posY, quantity):
        super().__init__(posX, posY)
        self.image = pg.image.load("../factory-game/iron_ore.png")
        self.is_player = False
        self.quantity = quantity
        self.item_name = None
        self.destruct_time = None

    def mine(self, miner):
        self.quantity -= 1
        miner.inventory.append((self.item_name, 1))
        self.player.set_message(f"Collected 1 {self.item_name}")
        if self.quantity == 0:
            self.world.remove_entity(self) 

class IronOre(Ore):
    def __init__(self, posX, posY, quantity):
        super().__init__(posX, posY, quantity)
        self.image = pg.image.load("../factory-game/iron_ore.png")
        self.item_name = "iron_ore"

class CopperOre(Ore):
    def __init__(self, posX, posY, quantity):
        super().__init__(posX, posY, quantity)
        self.image = pg.image.load("../factory-game/copper_ore.png")
        self.item_name = "copper_ore"
    

class Cursor(Entity):
    def __init__(self, posX, posY):
        super().__init__(posX, posY)
        self.image = pg.image.load("../factory-game/cursor.png")
        self.is_player = False