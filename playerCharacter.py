import pygame

from buffalo import utils

from camera import Camera
from character import Character
from chunk import Chunk

from inventory import Inventory

class PlayerCharacter(Character):

    DEFAULT_NAME  = "Unnamed PlayerCharacter"
    DEFAULT_SIZE  = 32, 64
    DEFAULT_SPEED = 0.02
    DEFAULT_FPOS  = (
        float(Chunk.CHUNK_WIDTH * Chunk.TILE_SIZE / 2 - DEFAULT_SIZE[0] / 2),
        float(Chunk.CHUNK_HEIGHT * Chunk.TILE_SIZE / 2 - DEFAULT_SIZE[1]),
        )
    DEFAULT_COLOR = (170,170,170,255) # Added for testing purposes

    #**kwargs here allows for an object to be created with a dictionary for input, which basically allows an object to be created from the deserialize method
    def __init__(self, inventory, name=None, fPos=None, size=None, speed=None, **kwargs):
        name = name if name is not None else PlayerCharacter.DEFAULT_NAME #These could probably be rewritten with kwargs
        fPos = fPos if fPos is not None else PlayerCharacter.DEFAULT_FPOS
        size = size if size is not None else PlayerCharacter.DEFAULT_SIZE
        Character.__init__(self, name=name, fPos=fPos, size=size)
        self.speed = speed if speed is not None else PlayerCharacter.DEFAULT_SPEED
        self.xv, self.yv = 0.0, 0.0
        self.surface = utils.empty_surface(self.size)
        self.inventory = inventory
        self.surface.fill(PlayerCharacter.DEFAULT_COLOR)

    def update(self, keys):

        if keys[pygame.K_w]:
            self.yv += -self.speed
        if keys[pygame.K_s]:
            self.yv += self.speed
        if keys[pygame.K_d]:
            self.xv += self.speed
        if keys[pygame.K_a]:
            self.xv += -self.speed

        x, y = self.fPos
        x += self.xv * utils.delta
        y += self.yv * utils.delta
        self.fPos = x, y
        self.pos  = int(self.fPos[0]), int(self.fPos[1])
        self.xv, self.yv = 0.0, 0.0

    def blit(self, dest):
        x, y = self.pos
        cx, cy = Camera.pos
        dest.blit(self.surface, (x - cx, y - cy))
