import quadTree

class Entity():
    def __init__(self, x, y, hp, stat):
        #self.name = ""
        self.x_pos = x
        self.y_pos = y
        self.health = hp
        self.attack = stat
        self.health_max = max
    
    def move_X(self, current_x, move_x):
        return current_x + move_x
    
    def move_Y(self, current_y, move_y):
        return current_y + move_y
    
    def get_X(self, x):
        return x
    
    def get_Y(self, y):
        return y