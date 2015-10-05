import sys

import pygame
from buffalo import utils
from buffalo.scene import Scene
from buffalo.label import Label

from saves import Saves
from chunk import Chunk
from camera import Camera
from mapManager import MapManager
from pluginManager import PluginManager

from playerCharacter import PlayerCharacter

class GameTestScene(Scene):
    def __init__(self, pc):
        Scene.__init__(self)
        self.BACKGROUND_COLOR = (0, 0, 0, 255)
        PluginManager.loadPlugins()
        Camera.init()
        pc = Saves.unstore(pc, "characters")
        self.pc = pc if pc is not None else PlayerCharacter(
                name="Sean",
                fPos=(float(utils.SCREEN_M[0]), float(utils.SCREEN_M[1])),
                size=(32, 64),
                speed=.25,
                color=(255,0,0,255),
            )
        Camera.lock(self.pc)
        MapManager.loadChunks(0,0)

    def on_escape(self):
        Saves.store(self.pc)
        sys.exit()

    def update(self):
        keys = pygame.key.get_pressed()
        self.pc.update(keys)
        Camera.update()

    def blit(self):
        Camera.blitView()
        self.pc.blit(utils.screen)
