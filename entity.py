

class Entity(object):
    
    entityIDCounter = 0
    
    def __init__(self, x, y):
        self.name = Entity.entityIDCounter
        Entity.entityIDCounter += 1
        self.id = Entity.entityIDCounter
        self.x = x
        self.y = y
        left = x - 1
        right = x + 1
        top = y - 1
        bottom = y + 1
        self.boundary_box = [left,top,right,bottom]
    
    def move_X(self, move_x):
        self.x += move_x
    
    def move_Y(self, move_y):
        self.y += move_y
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @x.setter
    def x(self, x):
        self._x = x
        
    @y.setter
    def y(self, y):
        self._y = y
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        return self.name == other.name
    
    def get_rect(self):
        return self.rect
    
    def __str__(self):
        return "entity " + (str)(self.id)