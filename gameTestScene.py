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
from inventoryUI import InventoryUI
from inventory import Inventory
from guiManager import GUIManager
from craftingUI import CraftingUI
from tradingUI import TradingUI

from playerCharacter import PlayerCharacter
from friendly import Friendly
from enemy import Enemy
from trader import Trader

class GameTestScene(Scene):
    def __init__(self, pc_name):
        Scene.__init__(self)
        self.BACKGROUND_COLOR = (0, 0, 0, 255)
        PluginManager.loadPlugins()
        Camera.init()
        self.enemy = Enemy(name="monster", fPos=(0.0,0.0)) # Example enemy
        self.friendly = Friendly(name="villager", fPos=(0.0,0.0)) # Example friendly npc
        self.trader = Trader(name="merchant", fPos=(0.0,0.0)) # Example trader
        self.npcs = [self.enemy, self.friendly, self.trader]
        self.pc = Saves.unstore(pc_name, "characters")
        self.npcs.detectCollisions()
        Camera.lock(self.pc)
        self.UIManager = GUIManager()
        self.UIManager.guiScreens.append(InventoryUI(self.pc.inventory, self.UIManager))
        self.UIManager.guiScreens.append(CraftingUI(self.pc.inventory))
        self.UIManager.updateGUIs()

    def on_escape(self):
        Saves.store(self.pc)
        sys.exit()

    def update(self):
        keys = pygame.key.get_pressed()
        self.pc.update(keys)
        for npc in self.npcs:
            if npc.__class__.__name__ is "Enemy":
                npc.update(self.pc.fPos)
            elif npc.__class__.__name__ is "Friendly":
                npc.update()
            elif npc.__class__.__name__ is "Trader":
                npc.update(self.pc.inventory, self.UIManager)
        self.UIManager.update()
        Camera.update()

    def blit(self):
        Camera.blitView()
        self.UIManager.blit(utils.screen, (0,0))
        self.pc.blit(utils.screen)
        for npc in self.npcs:
            npc.blit(utils.screen)
