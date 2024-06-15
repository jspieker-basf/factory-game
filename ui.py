import pygame as pg
from entities import *
import os
from time import time

class UIElement():
    def __init__(self, world):
        self.world = world

    def toggle(self):
        """
        Toggles the UI element on or off.
        """
        if self.visible:
            self.visible = False
        else:
            self.visible = True

class Grid(UIElement):
    def __init__(self, world):
        super().__init__(world)
        self.visible = False

    def render(self):
        if self.visible:
            # Render the grid
            centerPosX = self.world.surface.get_width() // 2
            centerPosY = self.world.surface.get_height() // 2
            ts = self.world.tile_size

            for x in range(centerPosX - ts * 15, centerPosX + ts * 15, ts):
                col = 'red' if x == centerPosX else 'yellow'
                pg.draw.line(self.world.surface, pg.Color(col), (x, 0), (x, self.world.surface.get_height()))
            for y in range(centerPosY - ts * 15, centerPosY + ts * 15, ts):
                col = 'red' if y == centerPosY else 'yellow'
                pg.draw.line(self.world.surface, pg.Color(col), (0, y), (self.world.surface.get_width(), y))

class InventoryBar(UIElement):
    def __init__(self, world):
        super().__init__(world)
        self.visible = True

    def render(self):
        if self.visible and self.world.player is not None:
            # Render the inventory bar
            inventory_bar_width = self.world.surface.get_width() // 2
            inventory_bar_height = self.world.surface.get_height() // 10
            inventory_slot_width = inventory_bar_width // 8

            # Render the inventory bar background
            inventory_bar_rect = pg.Rect(inventory_bar_width // 2, self.world.surface.get_height() - inventory_bar_height, inventory_bar_width, inventory_bar_height)
            pg.draw.rect(self.world.surface, pg.Color('gray'), inventory_bar_rect)

            # Render the inventory slots
            slot_rects = []
            for i in range(8):
                slot_rect = pg.Rect(inventory_bar_width // 2 + i * inventory_slot_width, self.world.surface.get_height() - inventory_bar_height, inventory_slot_width, inventory_bar_height)
                slot_rects.append(slot_rect)
                pg.draw.rect(self.world.surface, pg.Color('white'), slot_rect, 2)

            # Render the inventory items
            i = 0
            for item in self.world.player.inventory:
                slot_rect = slot_rects[i]
                item_img = item[0].icon if item[0].icon else item[0].image
                item_img = pg.transform.scale(item_img, (inventory_slot_width - 20, inventory_bar_height - 20))
                self.world.surface.blit(item_img, (slot_rect.x + 10, slot_rect.y + 10))
                self.world.surface.blit(self.world.font.render(str(item[1]), True, pg.Color('white'), pg.Color('black')), (slot_rect.x + 10, slot_rect.y + 10))
                i += 1

class SimpleMenu(UIElement):
    def __init__(self, world):
        super().__init__(world)
        self.visible = False

    def render(self):
        if self.visible:
            # Render the menu buttons
            button_width = 200
            button_height = 50
            button_padding = 20
            button_x = self.world.surface.get_width() // 2 - button_width // 2
            button_y = self.world.surface.get_height() // 2 - (button_height + button_padding) * 2

            resume_button_rect = pg.Rect(button_x, button_y, button_width, button_height)
            pg.draw.rect(self.world.surface, pg.Color('green'), resume_button_rect)
            self.world.surface.blit(self.world.font.render("Resume", True, pg.Color('white')), (resume_button_rect.x + 10, resume_button_rect.y + 10))

            save_button_rect = pg.Rect(button_x, button_y + button_height + button_padding, button_width, button_height)
            pg.draw.rect(self.world.surface, pg.Color('blue'), save_button_rect)
            self.world.surface.blit(self.world.font.render("Save", True, pg.Color('white')), (save_button_rect.x + 10, save_button_rect.y + 10))

            load_button_rect = pg.Rect(button_x, button_y + (button_height + button_padding) * 2, button_width, button_height)
            pg.draw.rect(self.world.surface, pg.Color('orange'), load_button_rect)
            self.world.surface.blit(self.world.font.render("Load", True, pg.Color('white')), (load_button_rect.x + 10, load_button_rect.y + 10))

            quit_button_rect = pg.Rect(button_x, button_y + (button_height + button_padding) * 3, button_width, button_height)
            pg.draw.rect(self.world.surface, pg.Color('red'), quit_button_rect)
            self.world.surface.blit(self.world.font.render("Quit", True, pg.Color('white')), (quit_button_rect.x + 10, quit_button_rect.y + 10))

            # Handle button clicks
            mouse_pos = pg.mouse.get_pos()
            if pg.mouse.get_pressed()[0]:
                if resume_button_rect.collidepoint(mouse_pos):
                    # Hide menu
                    self.visible = False
                elif save_button_rect.collidepoint(mouse_pos):
                    # Call the save function
                    self.visible = False
                    self.world.ui_save_game_selection.visible = True
                elif load_button_rect.collidepoint(mouse_pos):
                    # Call the load function
                    self.visible = False
                    self.world.ui_load_game_selection.visible = True
                elif quit_button_rect.collidepoint(mouse_pos):
                    # Call the quit function
                    self.visible = False
                    self.world.quit_game()

class LoadGameSelection(UIElement):
    def __init__(self, world):
        super().__init__(world)
        self.visible = False
        self.savegame_files = self.get_savegame_files()

    def render(self):
        if self.visible:
            # Get the list of savegame files
            print(self.savegame_files)
            # Render the savegame selection menu
            menu_width = 400
            menu_height = 300
            menu_x = self.world.surface.get_width() // 2 - menu_width // 2
            menu_y = self.world.surface.get_height() // 2 - menu_height // 2

            menu_rect = pg.Rect(menu_x, menu_y, menu_width, menu_height)
            pg.draw.rect(self.world.surface, pg.Color('white'), menu_rect)

            # Render the savegame file names
            text_padding = 5
            text_x = menu_x + text_padding
            text_y = menu_y + text_padding

            for i, savegame_file in enumerate(self.savegame_files):
                text_rect = pg.Rect(text_x, text_y + i * (self.world.font.get_height() + text_padding), menu_width - 2 * text_padding, self.world.font.get_height() + text_padding)
                pg.draw.rect(self.world.surface, pg.Color('lightgray'), text_rect)
                self.world.surface.blit(self.world.font.render(savegame_file, True, pg.Color('black')), (text_rect.x + text_padding, text_rect.y + text_padding))

            # Handle mouse clicks
            mouse_pos = pg.mouse.get_pos()
            if pg.mouse.get_pressed()[0]:
                for i, savegame_file in enumerate(self.savegame_files):
                    text_rect = pg.Rect(text_x, text_y + i * (self.world.font.get_height() + text_padding), menu_width - 2 * text_padding, self.world.font.get_height() + text_padding)
                    if text_rect.collidepoint(mouse_pos):
                        # Load the selected savegame file
                        self.visible = False
                        fp = os.path.join(self.folder_path, savegame_file)
                        print(f"load_game({fp})")
                        self.world.load_game(fp)

            # Handle key presses
            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                self.visible = False
                self.world.ui_menu.visible = True

    def get_savegame_files(self):
        """
        Returns a list of savegame files available for loading.
        """
        savegame_folder = "save"
        savegame_files = []

        # Get the list of files in the savegame folder
        self.folder_path = os.path.join(os.path.dirname(__file__), savegame_folder)
        print("folder_path", self.folder_path)
        if os.path.exists(self.folder_path) and os.path.isdir(self.folder_path):
            savegame_files = [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]

        return savegame_files

class SaveGameSelection(UIElement):
    def __init__(self, world):
        super().__init__(world)
        self.visible = False
        self.savegame_files = self.get_savegame_files()
        self.selected_file = None
        self.new_file_name = ""
        self.textbox_active = False

    def render(self):
        if self.visible:
            # Render the savegame selection menu
            menu_width = 400
            menu_height = 300
            menu_x = self.world.surface.get_width() // 2 - menu_width // 2
            menu_y = self.world.surface.get_height() // 2 - menu_height // 2

            menu_rect = pg.Rect(menu_x, menu_y, menu_width, menu_height)
            pg.draw.rect(self.world.surface, pg.Color('white'), menu_rect)

            # Render the savegame file names
            text_padding = 5
            text_x = menu_x + text_padding
            text_y = menu_y + text_padding

            for i, savegame_file in enumerate(self.savegame_files):
                text_rect = pg.Rect(text_x, text_y + i * (self.world.font.get_height() + text_padding), menu_width - 2 * text_padding, self.world.font.get_height() + text_padding)
                pg.draw.rect(self.world.surface, pg.Color('lightgray'), text_rect)
                self.world.surface.blit(self.world.font.render(savegame_file, True, pg.Color('black')), (text_rect.x + text_padding, text_rect.y + text_padding))

                if self.selected_file == savegame_file:
                    pg.draw.rect(self.world.surface, pg.Color('blue'), text_rect, 2)

            # Render the new file name textbox
            textbox_width = menu_width - 2 * text_padding
            textbox_height = self.world.font.get_height() + 10
            textbox_rect = pg.Rect(text_x, text_y + len(self.savegame_files) * (self.world.font.get_height() + text_padding) + 10, textbox_width, textbox_height)
            pg.draw.rect(self.world.surface, pg.Color('white'), textbox_rect, 2)
            # pg.draw.rect(self.world.surface, pg.Color('lightgray'), textbox_rect)
            self.world.surface.blit(self.world.font.render(self.new_file_name, True, pg.Color('black')), (textbox_rect.x + text_padding, textbox_rect.y + 5))

            # Render the save button
            save_button_rect = pg.Rect(text_x, textbox_rect.y + textbox_height + text_padding, textbox_width, textbox_height)
            pg.draw.rect(self.world.surface, pg.Color('green'), save_button_rect)
            self.world.surface.blit(self.world.font.render("Save", True, pg.Color('white')), (save_button_rect.x + 10, save_button_rect.y + 10))

            # Handle mouse clicks
            mouse_pos = pg.mouse.get_pos()
            if pg.mouse.get_pressed()[0]:
                for i, savegame_file in enumerate(self.savegame_files):
                    text_rect = pg.Rect(text_x, text_y + i * (self.world.font.get_height() + text_padding), menu_width - 2 * text_padding, self.world.font.get_height())
                    if text_rect.collidepoint(mouse_pos):
                        # Select the savegame file
                        self.selected_file = savegame_file

                if textbox_rect.collidepoint(mouse_pos):
                    # Clear the new file name textbox
                    self.new_file_name = ""
                    self.textbox_active = True

                if save_button_rect.collidepoint(mouse_pos):
                    # Save the game
                    if self.selected_file:
                        # Overwrite the selected savegame file
                        fp = os.path.join(self.folder_path, self.selected_file)
                        print(f"save_game({fp})")
                        self.world.save_game(fp)
                        self.visible = False
                    elif self.new_file_name:
                        # Save the game with a new file name
                        fp = os.path.join(self.folder_path, self.new_file_name)
                        print(f"save_game({fp})")
                        self.world.save_game(fp)
                        self.visible = False

            # Handle key presses
            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                self.visible = False
                self.world.ui_menu.visible = True

            if self.selected_file is None and self.textbox_active:
                # Handle typing in the new file name textbox
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            self.new_file_name = self.new_file_name[:-1]
                        else:
                            self.new_file_name += event.unicode

    def get_savegame_files(self):
        """
        Returns a list of savegame files available for overwriting.
        """
        savegame_folder = "save"
        savegame_files = []

        # Get the list of files in the savegame folder
        self.folder_path = os.path.join(os.path.dirname(__file__), savegame_folder)
        print("folder_path", self.folder_path)
        if os.path.exists(self.folder_path) and os.path.isdir(self.folder_path):
            savegame_files = [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]

        return savegame_files