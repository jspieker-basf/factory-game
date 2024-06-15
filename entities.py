import pygame as pg
import math

class Message():
    """
    Represents a message with content and expiration time.

    Attributes:
        content (str): The content of the message.
        expiration (datetime): The expiration time of the message.
    """

    def __init__(self, content, expiration):
        self.content = content
        self.expiration = expiration

class Inventory():
    """
    Represents an inventory with a limited number of slots for storing items.

    Attributes:
        slots (list): A list of slots in the inventory, where each slot is represented as a list containing an item and its quantity.
        max_slots (int): The maximum number of slots in the inventory.

    Methods:
        add_item(item, quantity): Adds an item to the inventory with the specified quantity.
        remove_item(item, quantity): Removes an item from the inventory with the specified quantity.
    """

    def __init__(self, max_slots):
        self.slots = []
        self.max_slots = max_slots

    def add_item(self, item: object, quantity: int) -> None:
        """
        Adds an item to the inventory with the specified quantity.

        Args:
            item (Entity): The item to be added.
            quantity (int): The quantity of the item to be added.

        Raises:
            Exception: If the inventory is full and there are no empty slots available.

        Returns:
            None
        """
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

    def remove_item(self, item: object, quantity: int) -> None:
        """
        Removes an item from the inventory with the specified quantity.

        Args:
            item (Entity): The item to be removed.
            quantity (int): The quantity of the item to be removed.

        Raises:
            Exception: If the item is not found in the inventory.

        Returns:
            None
        """
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

    def items(self):
        return self.slots

class Entity(pg.sprite.Sprite):
    """
    Represents an entity in the game world.

    Attributes:
        posX (int): The X position of the entity.
        posY (int): The Y position of the entity.
        world (World): The world the entity belongs to.
        id (int): The unique identifier of the entity.
        image (Surface): The image of the entity.
        icon (Surface): The icon of the entity.
        messages (list): The list of messages associated with the entity.
        size (tuple): The size of the entity.
        max_stack_size (int): The maximum stack size of the entity.
    """

    def __init__(self, posX: float, posY: float) -> None:
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

    def set_message(self, message: str) -> None:
        """
        Sets a new message for the entity.

        Parameters:
        - message (str): The message to be set.

        Returns:
        None
        """
        self.messages.insert(0, Message(message, self.world.time.get_ticks() + 2500))

    def render_messages(self) -> None:
        """
        Renders the messages on the game surface.

        This method iterates through the list of messages and renders each message on the game surface.
        It also removes any expired messages from the list.

        Args:
            None

        Returns:
            None
        """
        c_time = self.world.time.get_ticks()
        offset = 1
        self.messages = [message for message in self.messages if c_time < message.expiration]
        for message in self.messages:
            self.world.surface.blit(self.world.font.render(message.content, True, pg.Color('white')), (self.rect.left + 50 + 25 * offset, self.rect.top + 25 * -offset))
            offset += 1

    def render(self) -> None:
        """
        Renders the entity on the game surface.

        Raises:
            Exception: If the entity is not in a world or if it has no image.

        Notes:
            - If the entity is the player, the image is scaled to a fixed aspect ratio.
            - If the entity is not the player, the image is scaled based on its size.
            - The entity is blitted onto the game surface at the appropriate position.
            - If the entity has any messages, they are rendered as well.
            - The entity's rect attribute is updated to match the blitted position.
        """
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
    """
    Represents an engineer entity in the game.

    Attributes:
    - posX (float): The x-coordinate of the engineer's position.
    - posY (float): The y-coordinate of the engineer's position.
    - spritesheet (Surface): The spritesheet image of the engineer.
    - is_player (bool): Indicates whether the engineer is controlled by the player.
    - inventory (Inventory): The inventory of the engineer.

    Methods:
    - __init__(self, posX: float, posY: float) -> None: Initializes a new instance of the Engineer class.
    - move(self): Moves the engineer based on the user's input.
    - update_rotation(self, heading): Updates the engineer's rotation based on the heading angle.
    """

    def __init__(self, posX: float, posY: float, inventory: Inventory = None) -> None:
        super().__init__(posX, posY)
        self.spritesheet = pg.image.load("../factory-game/engineer_spritesheet.tga")
        self.update_rotation(-90)
        self.is_player = True
        if inventory:
            self.inventory = inventory
        else:
            self.inventory = Inventory(8)

    def move(self) -> None:
        """
        Move the entity based on the keyboard input.

        The entity's movement is determined by the keys pressed by the user.
        The entity can move in eight directions: left, right, up, down, and the four diagonal directions.

        Returns:
            None
        """
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

    def update_rotation(self, heading: int) -> None:
        """
        Update the rotation of the entity based on the given heading.

        Args:
            heading (int): The heading angle in degrees.

        Returns:
            None
        """
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
    """
    Represents a tile in the game world.

    Attributes:
        posX (int): The x-coordinate of the tile's position.
        posY (int): The y-coordinate of the tile's position.
        image (Surface): The image of the tile.
        is_player (bool): Indicates whether the tile is the player's tile.
    """

    def __init__(self, posX: float, posY: float) -> None:
        super().__init__(posX, posY)
        self.image = pg.image.load("../factory-game/sand.jpg")
        self.is_player = False

class Depletable(Entity):
    """
    Represents a depletable entity in the game.

    Attributes:
        posX (int): The x-coordinate of the entity's position.
        posY (int): The y-coordinate of the entity's position.
        quantity (int): The initial quantity of the depletable entity.
        image: The image representation of the entity.
        is_player (bool): Indicates whether the entity is the player.
        item_name: The name of the item associated with the entity.
    """

    def __init__(self, posX: float, posY: float, quantity: float) -> None:
        super().__init__(posX, posY)
        self.image = None
        self.is_player = False
        self.quantity = quantity
        self.item_name = None

    def mine(self, miner: Engineer) -> None:
        """
        Mines the depletable entity.

        Args:
            miner: The miner entity that is mining the depletable entity.
        """
        player_dist = pg.math.Vector2(self.posX, self.posY).distance_to((self.world.player.posX, self.world.player.posY))
        if player_dist < 5:
            self.quantity -= 1
            miner.inventory.add_item(self, 1)
            self.world.player.set_message(f"Collected 1 {self.item_name}")
            if self.quantity == 0:
                self.world.remove_entity(self)

class Mineable(Entity):
    """
    Represents a mineable entity in the game.

    Attributes:
        posX (int): The x-coordinate of the entity's position.
        posY (int): The y-coordinate of the entity's position.
        image: The image associated with the entity.
        is_player (bool): Indicates whether the entity is a player.
        item_name: The name of the item that can be mined from the entity.
        max_stack_size (int): The maximum stack size for the mined item.
        quantity (int): The quantity of the mined item.

    Methods:
        mine(miner): Mines the entity and adds the mined item to the miner's inventory.
    """

    def __init__(self, posX: float, posY: float) -> None:
        super().__init__(posX, posY)
        self.image = None
        self.is_player = False
        self.item_name = None
        self.max_stack_size = 64
        self.quantity = 1

    def mine(self, miner: Engineer) -> None:
        """
        Mines the entity and adds the mined item to the miner's inventory.

        Args:
            miner: The miner object that is mining the entity.

        Returns:
            None
        """
        player_dist = pg.math.Vector2(self.posX, self.posY).distance_to((self.world.player.posX, self.world.player.posY))
        if player_dist < 5:
            miner.inventory.add_item(self, self.quantity)
            self.world.player.set_message(f"Collected 1 {self.item_name}")
            self.world.remove_entity(self)

class IronOre(Depletable):
    def __init__(self, posX: float, posY: float, quantity: float) -> None:
        super().__init__(posX, posY, quantity)
        self.image = pg.image.load("../factory-game/iron_ore.png")
        self.item_name = "iron_ore"

class CopperOre(Depletable):
    def __init__(self, posX: float, posY: float, quantity: float) -> None:
        super().__init__(posX, posY, quantity)
        self.image = pg.image.load("../factory-game/copper_ore.png")
        self.item_name = "copper_ore"

class Coal(Depletable):
    def __init__(self, posX: float, posY: float, quantity: float) -> None:
        super().__init__(posX, posY, quantity)
        self.image = pg.image.load("../factory-game/coal.png")
        self.item_name = "coal"

class Tree(Mineable):
    def __init__(self, posX: float, posY: float) -> None:
        super().__init__(posX, posY)
        self.size = (4, 4)
        self.image = pg.image.load("../factory-game/tree.png")
        self.icon = pg.image.load("../factory-game/wood.png")
        self.is_player = False
        self.item_name = "wood"
        self.quantity = 5

class Cursor(Entity):
    def __init__(self, posX: float, posY: float) -> None:
        super().__init__(posX, posY)
        self.image = pg.image.load("../factory-game/cursor.png")
        self.is_player = False

class Oven(Mineable):
    def __init__(self, posX: float, posY: float) -> None:
        super().__init__(posX, posY)
        self.size = (2, 2)
        self.image = pg.image.load("../factory-game/oven.png")
        self.item_name = "oven"
        self.is_player = False