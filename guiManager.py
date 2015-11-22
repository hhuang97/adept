from buffalo import utils
from inventoryUI import InventoryUI
import pygame
from playerConsole import PlayerConsole

"""
Class to manage the in-game GUI. (i.e. Inventory and Crafting)
"""

class GUIManager:
	def __init__(self):
		self.active = False;
		self.surface = utils.empty_surface((utils.SCREEN_W, utils.SCREEN_H))
		self.alwaysOnSurface = utils.empty_surface((utils.SCREEN_W, utils.SCREEN_H))
		self.guiScreens = list()
		self.alwaysOnGUIs = list()
		self.keydown = False;
		self.mousedown = False;
		self.draggedItem = None

	def registerGUI(self,gui):
		if not hasattr(gui,'update') or not hasattr(gui,'mouseDown'):
			raise NotImplementedError
		self.guiScreens.append(gui)

	def registerAlwaysOnGUI(self,gui):
		if not hasattr(gui,'update') or not hasattr(gui,'mouseDown'):
			raise NotImplementedError
		self.alwaysOnGUIs.append(gui)

	def updateGUIs(self):
		"""
		Calls update on all the registered GUIs
		"""
		self.surface = utils.empty_surface((utils.SCREEN_W, utils.SCREEN_H))
		self.alwaysOnSurface = utils.empty_surface((utils.SCREEN_W, utils.SCREEN_H))
		for UIObject in self.guiScreens:
			if not hasattr(UIObject, 'update'):
				raise NotImplementedError
			UIObject.update()
			self.surface.blit(UIObject.surface, UIObject.pos)
		for UIObject in self.alwaysOnGUIs:
			if not hasattr(UIObject, 'update'):
				raise NotImplementedError
			UIObject.update()
			self.alwaysOnSurface.blit(UIObject.surface, UIObject.pos)

	def findCollidingGUI(self, pos):
		"""
		Given a position (such as a mouse click) find the GUI screen that the position interacts with.
		"""
		for UIObject in self.guiScreens:
			if not hasattr(UIObject,'pos'):
				raise UserWarning
			guiPos = UIObject.pos
			guiRect = pygame.Rect(guiPos, (UIObject.surface.get_size()))
			if guiRect.collidepoint(pos):
				return UIObject
		return None

	def update(self):
		#Keyboard Events
		keys = pygame.key.get_pressed()
		if keys[pygame.K_e]:
			self.updateGUIs()
			#On Keydown
			if not self.keydown:
				self.active = not self.active
				self.keydown = True
		else:
			self.keydown = False


		if self.active:
			PlayerConsole.flashOn()
			for gui in self.guiScreens:
				if hasattr(gui, "handleKeyboardPress"):
					if gui.handleKeyboardPress(keys) is not None:
						self.updateGUIs()
		else:
			for gui in self.alwaysOnGUIs:
				if hasattr(gui, "handleKeyboardPress"):
					if gui.handleKeyboardPress(keys) is not None:
						self.updateGUIs()
			return

		#Mouse Events
		if pygame.mouse.get_pressed()[0]:
			self.updateGUIs()
			#On Mousedown
			if not self.mousedown:
				self.mousedown = True
				UIObject = self.findCollidingGUI(pygame.mouse.get_pos())
				if UIObject != None:
					if not hasattr(UIObject,'mouseDown'):
						raise NotImplementedError
					absLocation = pygame.mouse.get_pos()
					relLocation = (absLocation[0] - UIObject.pos[0], absLocation[1] - UIObject.pos[1])
					UIObject.mouseDown(relLocation)
					self.updateGUIs()

		else:
			self.mousedown = False

	def blit(self, dest, pos):
		if(self.active):
			dest.blit(self.surface, pos)
		else:
			dest.blit(self.alwaysOnSurface, pos)
		if self.draggedItem != None:
			newPos = (pygame.mouse.get_pos()[0] - InventoryUI.BUTTON_SIZE / 2, 
				pygame.mouse.get_pos()[1] - InventoryUI.BUTTON_SIZE / 2)
			dest.blit(self.draggedItem.surface, newPos)