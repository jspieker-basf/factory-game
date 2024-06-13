import pygame as pg
from entities import *

class World:
    def __init__(self, name, surface, time, font) -> None:
        self.name = name
        self.entities = []
        self.player = None
        self.surface = surface
        self.tile_size = surface.get_width() // 20
        self.time = time
        self.font = font
        self.debug_grid = False

    def toggle_grid(self):
        if self.debug_grid:
            self.debug_grid = False
        else:
            self.debug_grid = True

    def add_entities(self, entities):
        for entity in entities:
            self.entities.append(entity)
            entity.world = self
            if entity.is_player:
                self.player = entity

    def remove_entity(self, entity):
        entity.world = None
        self.entities.remove(entity)
        if entity.is_player:
            self.player = None

    def render(self):
        # Render the world
        for entity in self.entities:
            entity.render()

        if self.debug_grid:
            # Render the grid
            centerPosX = self.surface.get_width() // 2
            centerPosY = self.surface.get_height() // 2
            ts = self.tile_size

            for x in range(centerPosX - ts * 15, centerPosX + ts * 15, ts):
                col = 'red' if x == centerPosX else 'yellow'
                pg.draw.line(self.surface, pg.Color(col), (x, 0), (x, self.surface.get_height()))
            for y in range(centerPosY - ts * 15, centerPosY + ts * 15, ts):
                col = 'red' if y == centerPosY else 'yellow'
                pg.draw.line(self.surface, pg.Color(col), (0, y), (self.surface.get_width(), y))

        # Render the inventory bar
        inventory_bar_width = self.surface.get_width() // 2
        inventory_bar_height = self.surface.get_height() // 10
        inventory_slot_width = inventory_bar_width // 8

        # Render the inventory bar background
        inventory_bar_rect = pg.Rect(inventory_bar_width // 2, self.surface.get_height() - inventory_bar_height, inventory_bar_width, inventory_bar_height)
        pg.draw.rect(self.surface, pg.Color('gray'), inventory_bar_rect)

        # Render the inventory slots
        slot_rects = []
        for i in range(8):
            slot_rect = pg.Rect(inventory_bar_width // 2 + i * inventory_slot_width, self.surface.get_height() - inventory_bar_height, inventory_slot_width, inventory_bar_height)
            slot_rects.append(slot_rect)
            pg.draw.rect(self.surface, pg.Color('white'), slot_rect, 2)

        # Render the inventory items
        i = 0
        for item in self.player.inventory:
            slot_rect = slot_rects[i]
            item_img = item[0].icon if item[0].icon else item[0].image
            item_img = pg.transform.scale(item_img, (inventory_slot_width - 20, inventory_bar_height - 20))
            self.surface.blit(item_img, (slot_rect.x + 10, slot_rect.y + 10))
            self.surface.blit(self.font.render(str(item[1]), True, pg.Color('white'), pg.Color('black')), (slot_rect.x + 10, slot_rect.y + 10))
            i += 1


    def cursor(self, clicked_sprites, mouse_status):
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
