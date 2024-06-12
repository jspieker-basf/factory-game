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

    def add_entity(self, entity):
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

        # Render the grid
        centerPosX = self.surface.get_width() // 2
        centerPosY = self.surface.get_height() // 2
        ts = self.tile_size

        for x in range(centerPosX - ts * 15, centerPosX + ts * 15, ts):
            col = 'red' if x == centerPosX else 'grey'
            pg.draw.line(self.surface, pg.Color(col), (x, 0), (x, self.surface.get_height()))
        for y in range(centerPosY - ts * 15, centerPosY + ts * 15, ts):
            col = 'red' if y == centerPosY else 'grey'
            pg.draw.line(self.surface, pg.Color(col), (0, y), (self.surface.get_width(), y))

    def cursor(self, clicked_sprites):
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
            if isinstance(entity, Engineer):
                entity.set_message(f"Selected tile: {cursorWorldPosX}, {cursorWorldPosY}")
            if isinstance(entity, Ore):
                entity.mine(self.player)
            if entity.posX == cursorWorldPosX and entity.posY == cursorWorldPosY:
                # print(entity.__repr__(),"at cursor position")
                blitX = centerPosX + entity.posX * ts
                blitY = centerPosY - entity.posY * ts 
                self.surface.blit(pg.transform.scale(pg.image.load("../factory-game/cursor.png"),[ts, ts]), (blitX, blitY))
