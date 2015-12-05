from quadtree import QuadTree

class Manager(QuadTree):

    def __init__(self, boundary_box, max_entities=10, maxdepth=20):
        x1, y1, x2, y2 = boundary_box
        width, height = x2 - x1, y2 - y1
        midx, midy = x1 + width / 2.0, y1 + height / 2.0
        self.nodes = []
        self.children = []
        self.center = [midx, midy]
        self.width, self.height = width, height
        self.depth = 0
        self.max_entities = max_entities
        self.maxdepth = maxdepth

    def insert(self, entity, boundary_box):
        self._insert(entity, boundary_box)

    def intersect(self, boundary_box):
        return self._intersect(boundary_box)
    
    def count_members(self):
        size = 0
        for child in self.children:
            size += child.count_members()
        size += len(self.nodes)
        return size