import pygame as pg
from entities import *
import sqlite3
from ui import *

class World:
    """
    Represents the game world.

    Attributes:
        name (str): The name of the world.
        entities (list): A list of entities in the world.
        player (Entity): The player entity.
        surface (Surface): The surface to render the world on.
        tile_size (int): The size of each tile in pixels.
        time (int): The current time in the world.
        font (Font): The font used for rendering text.
        debug_grid (bool): Flag indicating whether to render the debug grid.
    """

    def __init__(self, name, surface, time, font) -> None:
        """
        Initializes a new instance of the World class.

        Args:
            name (str): The name of the world.
            surface (Surface): The surface to render the world on.
            time (int): The current time in the world.
            font (Font): The font used for rendering text.
        """
        self.name = name
        self.entities = []
        self.player = None
        self.surface = surface
        self.tile_size = surface.get_width() // 20
        self.time = time
        self.font = font
        self.paused = False
        self.ui = []
        self.world_saved = False
        self.current_save_fp = None

    def init_db(self, file_path: str, new_db: bool = False) -> bool:
        self.db_con = sqlite3.connect(file_path)
        self.db_cur = self.db_con.cursor()
        if not new_db:
            if not os.path.isfile(file_path):
                print("File does not exist.")
                return False
        print("Database opened successfully")

        # Check if entities table exists
        self.db_cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='entities'")
        table_exists = self.db_cur.fetchone()
        if not table_exists:
            self.db_cur.execute("CREATE TABLE entities (id INTEGER PRIMARY KEY, type TEXT, posX INTEGER, posY INTEGER, quantity INTEGER)")
            print("Table entities created successfully")

        # Check if player_inventory table exists
        self.db_cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='player_inventory'")
        table_exists = self.db_cur.fetchone()
        if not table_exists:
            self.db_cur.execute("CREATE TABLE player_inventory (id INTEGER PRIMARY KEY, item TEXT, quantity INTEGER)")
            print("Table player_inventory created successfully")
        return True

    def add_entities(self, entities):
        """
        Adds entities to the world.

        Args:
            entities (list): A list of entities to add.
        """
        for entity in entities:
            self.entities.append(entity)
            entity.world = self
            if entity.is_player:
                self.player = entity

    def remove_entity(self, entity):
        """
        Removes an entity from the world.

        Args:
            entity (Entity): The entity to remove.
        """
        entity.world = None
        self.entities.remove(entity)
        if entity.is_player:
            self.player = None

    def render(self):
        """
        Renders the world. Each entity is rendered in turn, and the debug grid is rendered if enabled.
        Then UI is rendered.
        """
        # Render the world
        for entity in self.entities:
            entity.render()

        # Render the UI
        for element in self.ui_elements:
            element.render()

    def cursor(self, clicked_sprites, mouse_status):
        """
        Handles cursor interaction.

        Args:
            clicked_sprites (list): A list of sprites that were clicked.
            mouse_status (tuple): A tuple representing the state of the mouse buttons.

        Returns:
            None
        """
        left, middle, right = mouse_status
        centerPosX = self.surface.get_width() // 2
        centerPosY = self.surface.get_height() // 2
        ts = self.tile_size

        # Render the cursor
        x, y = pg.mouse.get_pos()

        #calculate world postion of cursor
        cursorWorldPosX = (x - centerPosX) // ts
        cursorWorldPosY = (centerPosY - y) // ts + 1
        # print("selected tile:",cursorWorldPosX, cursorWorldPosY)
        for entity in clicked_sprites:
            print(entity.__repr__())
            if isinstance(entity, Engineer) and left:
                entity.set_message(f"Engineer at {cursorWorldPosX}, {cursorWorldPosY} :)")
            if isinstance(entity, (Depletable, Mineable)) and right:
                entity.mine(self.player)
            if isinstance(entity, Oven) and left:
                entity.set_message(f"Ich bin ein ofen, füttere mich!")
            if entity.posX == cursorWorldPosX and entity.posY == cursorWorldPosY:
                # print(entity.__repr__(),"at cursor position")
                blitX = centerPosX + entity.posX * ts
                blitY = centerPosY - entity.posY * ts
                self.surface.blit(pg.transform.scale(pg.image.load("../factory-game/cursor.png"),[ts, ts]), (blitX, blitY))

    def save_game(self, file_path: str) -> None:
        """
        Saves the game state to a file.
        """
        if not file_path.endswith(".db"):
            file_path += ".db"
        self.init_db(file_path, new_db=True) # initialize the database connection
        # Save entities
        try:
            self.db_cur.execute("DELETE FROM entities")
            for entity in self.entities:
                quantity = entity.quantity if hasattr(entity, "quantity") else -1
                self.db_cur.execute("INSERT INTO entities (type, posX, posY, quantity) VALUES (?, ?, ?, ?)", (entity.__class__.__name__, entity.posX, entity.posY, quantity))
            self.db_con.commit()
            print("Game saved successfully.")
        except sqlite3.OperationalError:
            print("Saving failed. entities table not found.")

        # Save player inventory
        try:
            self.db_cur.execute("DELETE FROM player_inventory")
            for item in self.player.inventory.items():
                self.db_cur.execute("INSERT INTO player_inventory (item, quantity) VALUES (?, ?)", (item[0].__class__.__name__, item[1]))
            self.db_con.commit()
            print("Inventory saved successfully.")
        except sqlite3.OperationalError:
            print("Saving failed. player_inventory table not found.")

    def load_game(self, file_path: str) -> None:
        """
        Loads the game state from a file.
        """
        self.init_db(file_path) # initialize the database connection
        # helper function for loading the inventory
        def load_inventory() -> Inventory:
            try:
                self.db_cur.execute("SELECT * FROM player_inventory")
                inventory = self.db_cur.fetchall()
                print("loaded inventory:", inventory)
                new_inventory = Inventory(8)
                for item in inventory:
                    if item[1] == "Oven":
                        new_inventory.add_item(Oven(0, 0), item[2])
                    elif item[1] == "CopperOre":
                        new_inventory.add_item(Copper_Ore(0, 0, 0), item[2])
                    elif item[1] == "IronOre":
                        new_inventory.add_item(Iron_Ore(0, 0, 0), item[2])
                    elif item[1] == "Coal":
                        new_inventory.add_item(Coal(0, 0, 0), item[2])
                    elif item[1] == "Tree":
                        new_inventory.add_item(Tree(0, 0), item[2])
                    else:
                        raise ValueError(f"Item type not found: {item[1]}")
                return new_inventory
            except sqlite3.OperationalError:
                print("Loading failed. player_inventory table not found. Please save the game first.")

        # helper function for loading the entities
        def load_entities() -> None:
            self.entities = []
            try:
                self.db_cur.execute("SELECT * FROM entities")
                entities = self.db_cur.fetchall()
                entity_types = {}
                for entity in entities:
                    if entity[1] not in entity_types:
                        entity_types[entity[1]] = 1
                    else:
                        entity_types[entity[1]] += 1
                print(f"loaded {len(entities)} entities. Types: {entity_types}")
                for entity in entities:
                    if entity[1] == "Engineer":
                        self.add_entities([Engineer(entity[2], entity[3], load_inventory())])
                    elif entity[1] == "Oven":
                        self.add_entities([Oven(entity[2], entity[3])])
                    elif entity[1] == "CopperOre":
                        self.add_entities([Copper_Ore(entity[2], entity[3], entity[4])])
                    elif entity[1] == "IronOre":
                        self.add_entities([Iron_Ore(entity[2], entity[3], entity[4])])
                    elif entity[1] == "Coal":
                        self.add_entities([Coal(entity[2], entity[3], entity[4])])
                    elif entity[1] == "Tree":
                        self.add_entities([Tree(entity[2], entity[3])])
                    elif entity[1] == "Tile":
                        self.add_entities([Tile(entity[2], entity[3])])
                    else:
                        raise ValueError(f"Entity type not found: {entity[1]}")
            except sqlite3.OperationalError:
                print("Loading failed. entities not found. Please save the game first.")

        # Load entities and inventory
        load_entities()

    def quit_game(self):
        """
        Quits the game.
        """
        self.db_con.close() # close the database connection
        pg.quit() # quit pygame
        quit() # quit python

    def init_ui(self):
        """
        Initializes the UI elements.
        """
        self.ui_grid = Grid(self)
        self.ui_inventory_bar = Inventory_Bar(self)
        self.ui_menu = Simple_Menu(self)
        self.ui_load_game_selection = Load_Game_Selection(self)
        self.ui_save_game_selection = Save_Game_Selection(self)

        self.ui_elements = [self.ui_grid,
                            self.ui_inventory_bar,
                            self.ui_menu,
                            self.ui_load_game_selection,
                            self.ui_save_game_selection]