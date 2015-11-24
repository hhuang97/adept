import os
import sys

from multiprocessing import Queue

import pygame

from buffalo import utils
from buffalo.scene import Scene
from buffalo.label import Label
from buffalo.button import Button
from buffalo.option import Option

from mapManager import MapManager
from inventory import Inventory
from saves import Saves
from gameTestScene import GameTestScene


class Menu(Scene):

    def on_escape(self):
        MapManager.soft_load_reader_queue = Queue()
        MapManager.soft_load_reader_queue.put("DONE")
        sys.exit()

    def update(self):
        pass

    def blit(self):
        pass

    def __init__(self):
        Scene.__init__(self)
        self.BACKGROUND_COLOR = (177, 0, 50, 255)
        Button.DEFAULT_BG_COLOR = (100, 100, 100, 255)
        Button.DEFAULT_FONT = "default18"
        Option.DEFAULT_FONT = "default18"
        self.labels.add(
            Label(
                (5, 5),
                "Adept 0.0 Alpha <-> September 2015",
            )
        )
        self.labels.add(
            Label(
                utils.SCREEN_M,
                "",
                font="default48",
                x_centered=True,
                y_centered=True,
            )
        )
        self.buttons.add(
            Button(
                (10, utils.SCREEN_H - 10),
                "Create New Character",
                invert_y_pos = True,
                func=self.go_to_createCharacter
            )
        )        
        self.buttons.add(
            Button(
                (utils.SCREEN_W / 2, utils.SCREEN_H / 2 + 160),
                "New Solo Game",
                x_centered=True,
                y_centered=True,
                func=self.go_to_gameTestScene,
            )
        )
        self.buttons.add(
            Button(
                (utils.SCREEN_W / 2, utils.SCREEN_H / 2 + 220),
                "Load Solo Game",
                x_centered=True,
                y_centered=True,
            )
        )
        self.buttons.add(
            Button(
                (utils.SCREEN_W - 10, utils.SCREEN_H - 10),
                "Join Multiplayer Game",
                invert_x_pos=True,
                invert_y_pos=True,
            )
        )
        self.buttons.add(
            Button(
                (utils.SCREEN_W / 2, utils.SCREEN_H / 2 + 280),
                "Options",
                x_centered=True,
                y_centered=True,
                func=self.go_to_options,
            )
        )
        self.buttons.add(
            Button(
                (utils.SCREEN_W / 2, utils.SCREEN_H / 2 + 340),
                "Exit",
                x_centered=True,
                y_centered=True,
                func=exit,
            )
        )
        #Creates selection option if characters exist
        if self.getNumCharacters() > 0:
            self.characterOption = Option(
                    (utils.SCREEN_W / 2, utils.SCREEN_H / 2 + 100),
                    self.getCharacterNames(),
                    x_centered=True,
                    y_centered=True,
                )
            self.options.add(self.characterOption)
        #
        else:
            self.labels.add(
                Label(
                (utils.SCREEN_W / 2, utils.SCREEN_H / 2 + 100),
                "No Characters",
                font=Option.DEFAULT_FONT,
                x_centered=True,
                y_centered=True,
                )
            )
        

    def getCharacterNames(self):
        if not self.getCharacters():
            return ["No Characters"]
        return self.getCharacters()

    def getCharacters(self):
        characters = list()
        if not os.path.isdir("characters"):
            os.mkdir("characters")
        for character in os.listdir("characters"):
            if character != ".DS_Store":
                characters.append(character)
        return characters

    def getNumCharacters(self):
        return len(self.getCharacters())

    def go_to_createCharacter(self):
        from createCharacter import CreateCharacter
        utils.set_scene(
            CreateCharacter()
        )
    def go_to_options(self):
        from options import Options
        utils.set_scene(
            Options()
        )
    def go_to_gameTestScene(self):
        if self.getNumCharacters() == 0:
            return

        pc_name = self.characterOption.label.text        

        MapManager.soft_load_reader_queue = Queue()
        MapManager.soft_load_reader_queue.put("DONE")

        utils.set_scene(
            GameTestScene(
                pc_name
            )
        )
