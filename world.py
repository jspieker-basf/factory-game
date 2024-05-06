import pygame as pg


class World:
    def __init__(self, name, surface) -> None:
        self.name = name
        self.entities = []
        self.player = None
        self.relative_position = (0, 0)
        self.screen_center = (surface.get_width()//2, surface.get_height()//2)
        self.zoom_level = 1 # 1 = 100% zoom, 20 = 5% zoom
        self.tile_size = surface.get_width() // self.zoom_level

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

    def setRelativePosition(self, pos):
        # camera position is the center of the screen
        self.relative_position = (pos[0] / self.zoom_level, pos[1] / self.zoom_level)

    def zoom(self, amount):
        if self.zoom_level + amount >= 1 and self.zoom_level + amount <= 80: # min 5 max 80 (tiles from center visible)
            self.zoom_level += amount

    def render(self, surface):
        # Render the world
        # w, h = surface.get_size()
        # zoom_factor = (w/self.zoom_level, h/self.zoom_level)
        for entity in self.entities:
            entity.render(surface, self.relative_position, self.screen_center, self.zoom_level)

        # Render the UI
