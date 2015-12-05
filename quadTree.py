from entity import Entity


def normalize_rect(rect):
    x1, y1, x2, y2 = rect
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    return (x1, y1, x2, y2)

class Node(Entity):
    
    def __init__(self, entity, rect):
        self.entity = entity
        self.rect = rect


class QuadTree:

    def __init__(self, x, y, width, height, depth=0, max_entities=4, maxdepth=20):
        # bounds are inclusive
        self.nodes = []
        self.children = []
        self.center = [x, y]
        self.width, self.height = width, height
        self.depth = depth
        self.max_entities = max_entities
        self.maxdepth = maxdepth
        
    def __iter__(self):
        def loop_all_children(parent):
            for child in parent.children:
                if child.children:
                    for subchild in loop_all_children(parent=child):
                        yield subchild
                yield child
        for child in loop_all_children(self):
            yield child
            
    def _insert(self, entity, boundary_box):
        rect = normalize_rect(boundary_box)
        if len(self.children) == 0:
            node = Node(entity, rect)
            self.nodes.append(node)
            
            if len(self.nodes) > self.max_entities and self.depth < self.maxdepth:
                self._split()
        else:
            self._insert_into_children(entity, rect)
            
    def _intersect(self, boundary_box, results=None): # finds all entities within a rectangle
        rect = boundary_box
        if results is None:
            rect = normalize_rect(rect)
            results = set()
        if len(self.children) > 0:
            if rect[0] <= self.center[0]:
                if rect[1] <= self.center[1]:
                    self.children[0]._intersect(rect, results)
                if rect[3] > self.center[1]:
                    self.children[1]._intersect(rect, results)
            if rect[2] > self.center[0]:
                if rect[1] <= self.center[1]:
                    self.children[2]._intersect(rect, results)
                if rect[3] > self.center[1]:
                    self.children[3]._intersect(rect, results)
        for node in self.nodes:
            if (node.rect[2] > rect[0] and node.rect[0] <= rect[2] and 
                node.rect[3] > rect[1] and node.rect[1] <= rect[3]):
                results.add(node.entity)
        return results


    def _insert_into_children(self, entity, rect): # if rect spans center then insert here
        if ((rect[0] <= self.center[0] and rect[2] > self.center[0]) and
            (rect[1] <= self.center[1] and rect[3] > self.center[1])):
            node = Node(entity, rect)
            self.nodes.append(node)
        else: # try to insert into children
            if rect[0] <= self.center[0]:
                if rect[1] <= self.center[1]:
                    self.children[0]._insert(entity, rect)
                if rect[3] > self.center[1]:
                    self.children[1]._insert(entity, rect)
            if rect[2] > self.center[0]:
                if rect[1] <= self.center[1]:
                    self.children[2]._insert(entity, rect)
                if rect[3] > self.center[1]:
                    self.children[3]._insert(entity, rect)
                    
    def _split(self):
        quartwidth = self.width / 4.0
        quartheight = self.height / 4.0
        halfwidth = self.width / 2.0
        halfheight = self.height / 2.0
        self.children = [QuadTree(self.center[0] - quartwidth,
                                  self.center[1] - quartheight,
                                  width=halfwidth, height=halfheight,
                                  depth=self.depth + 1,
                                  max_entities=self.max_entities,
                                  maxdepth=self.maxdepth),
                         QuadTree(self.center[0] - quartwidth,
                                  self.center[1] + quartheight,
                                  width=halfwidth, height=halfheight,
                                  depth=self.depth + 1,
                                  max_entities=self.max_entities,
                                  maxdepth=self.maxdepth),
                         QuadTree(self.center[0] + quartwidth,
                                  self.center[1] - quartheight,
                                  width=halfwidth, height=halfheight,
                                  depth=self.depth + 1,
                                  max_entities=self.max_entities,
                                  maxdepth=self.maxdepth),
                         QuadTree(self.center[0] + quartwidth,
                                  self.center[1] + quartheight,
                                  width=halfwidth, height=halfheight,
                                  depth=self.depth + 1,
                                  max_entities=self.max_entities,
                                  maxdepth=self.maxdepth)]
        nodes = self.nodes
        self.nodes = []
        for node in nodes:
            self._insert_into_children(node.entity, node.rect)

    def _remove(self, Entity):
        pass