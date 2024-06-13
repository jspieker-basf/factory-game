import pygame as pg
import math

class Message():
    def __init__(self, content, expiration):
        self.content = content
        self.expiration = expiration

class Inventory():
    def __init__(self, max_slots):
        self.slots = []
        self.max_slots = max_slots

    def add_item(self, item, quantity):
        for slot in self.slots:
            if slot[0].item_name == item.item_name and slot[1] < item.max_stack_size:
                space_left = item.max_stack_size - slot[1]
                if quantity <= space_left:
                    slot[1] += quantity
                    return
                else:
                    slot[1] = item.max_stack_size
                    quantity -= space_left
        empty_slots = self.max_slots - len(self.slots)
        if empty_slots > 0:
            if quantity <= item.max_stack_size:
                self.slots.append([item, quantity])
                return
            else:
                num_stacks = quantity // item.max_stack_size
                remainder = quantity % item.max_stack_size
                for _ in range(num_stacks):
                    self.slots.append([item, item.max_stack_size])
                if remainder > 0:
                    self.slots.append([item, remainder])
                return
        raise Exception("Inventory is full")


    def remove_item(self, item, quantity):
        for slot in self.slots:
            if slot[0] == item:
                if slot[1] > quantity:
                    slot[1] -= quantity
                    return
                elif slot[1] == quantity:
                    self.slots.remove(slot)
                    return
                else:
                    quantity -= slot[1]
                    self.slots.remove(slot)
        raise Exception("Item not found in inventory")

    def __iter__(self):
        return iter(self.slots)

class Entity(pg.sprite.Sprite):
    def __init__(self, posX, posY):
        super().__init__()
        self.posX = posX
        self.posY = posY
        self.world = None
        self.id = id(self)
        self.image = None
        self.icon = None
        self.messages = []
        self.size = (1, 1)
        self.max_stack_size = 64

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
                self.image = pg.transform.scale(self.image, [self.world.tile_size * self.size[0], self.world.tile_size * self.size[1]])
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
        self.is_player = True
        self.inventory = Inventory(8)

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
            self.update_rotation(heading)

    def update_rotation(self, heading):
        if heading == 0:
            self.image = self.spritesheet.subsurface((256*3, 0, 148, 512))
        elif heading == 45:
            self.image = self.spritesheet.subsurface((256*2, 512, 148, 512))
        elif heading == 90:
            self.image = self.spritesheet.subsurface((0, 512, 148, 512))
        elif heading == 135:
            self.image = self.spritesheet.subsurface((256, 512, 148, 512))
        elif heading == 180:
            self.image = self.spritesheet.subsurface((256*3, 512, 148, 512))
        elif heading == -135:
            self.image = self.spritesheet.subsurface((256*2, 0, 148, 512))
        elif heading == -90:
            self.image = self.spritesheet.subsurface((0, 0, 148, 512))
        elif heading == -45:
            self.image = self.spritesheet.subsurface((256, 0, 148, 512))

class Tile(Entity):
    def __init__(self, posX, posY):
        super().__init__(posX, posY)
        self.image = pg.image.load("../factory-game/sand.jpg")
        self.is_player = False

class Depletable(Entity):
    def __init__(self, posX, posY, quantity):
        super().__init__(posX, posY)
        self.image = None
        self.is_player = False
        self.quantity = quantity
        self.item_name = None

    def mine(self, miner):
        player_dist = pg.math.Vector2(self.posX, self.posY).distance_to((self.world.player.posX, self.world.player.posY))
        if player_dist < 5:
            self.quantity -= 1
            miner.inventory.add_item(self, 1)
            self.world.player.set_message(f"Collected 1 {self.item_name}")
            if self.quantity == 0:
                self.world.remove_entity(self)

class Mineable(Entity):
    def __init__(self, posX, posY):
        super().__init__(posX, posY)
        self.image = None
        self.is_player = False
        self.item_name = None
        self.max_stack_size = 64
        self.quantity = 1

    def mine(self, miner):
        player_dist = pg.math.Vector2(self.posX, self.posY).distance_to((self.world.player.posX, self.world.player.posY))
        if player_dist < 5:
            miner.inventory.add_item(self, self.quantity)
            self.world.player.set_message(f"Collected 1 {self.item_name}")
            self.world.remove_entity(self)

class IronOre(Depletable):
    def __init__(self, posX, posY, quantity):
        super().__init__(posX, posY, quantity)
        self.image = pg.image.load("../factory-game/iron_ore.png")
        self.item_name = "iron_ore"

class CopperOre(Depletable):
    def __init__(self, posX, posY, quantity):
        super().__init__(posX, posY, quantity)
        self.image = pg.image.load("../factory-game/copper_ore.png")
        self.item_name = "copper_ore"

class Coal(Depletable):
    def __init__(self, posX, posY, quantity):
        super().__init__(posX, posY, quantity)
        self.image = pg.image.load("../factory-game/coal.png")
        self.item_name = "coal"

class Tree(Mineable):
    def __init__(self, posX, posY):
        super().__init__(posX, posY)
        self.size = (4, 4)
        self.image = pg.image.load("../factory-game/tree.png")
        self.icon = pg.image.load("../factory-game/wood.png")
        self.is_player = False
        self.item_name = "wood"
        self.quantity = 5

class Cursor(Entity):
    def __init__(self, posX, posY):
        super().__init__(posX, posY)
        self.image = pg.image.load("../factory-game/cursor.png")
        self.is_player = False

class Oven(Mineable):
    def __init__(self, posX, posY):
        super().__init__(posX, posY)
        self.size = (2, 2)
        self.image = pg.image.load("../factory-game/oven.png")
        self.item_name = "oven"
        self.is_player = False