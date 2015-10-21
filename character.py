from serializable import Serializable
from Entity import Entity

from buffalo import utils

class Character(Serializable, Entity):

    DEFAULT_NAME = "Unnamed Character"
    DEFAULT_FPOS = float(utils.SCREEN_M[0]), float(utils.SCREEN_M[1])
    DEFAULT_SIZE = 32, 32
    
    def __init__(self, name=None, fPos=None, size=None):
        Entity.__init__(self, float(utils.SCREEN_M[0]), float(utils.SCREEN_M[1]))
        self.name = name if name is not None else Character.DEFAULT_NAME
        self.fPos = fPos if fPos is not None else Character.DEFAULT_FPOS
        self.size = size if size is not None else Character.DEFAULT_SIZE

    def update(self):
        raise NotImplementedError