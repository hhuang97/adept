class Node():
    ROOT = 0
    BRANCH = 1
    LEAF = 2
    minsize = 1
    
    def __init__(self, parent, rect):
        self.parent = parent
        self.children = [None,None,None,None]
        if parent == None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1
        self.rect = rect
        x0, x1 = rect
        if self.parent == None:
            self.type = Node.ROOT
        elif (x1 - x0) <= Node.minsize:
            self.type = Node.LEAF
        else:
            self.type = Node.BRANCH
   
    def subdivide(self):
        if self.type == Node.LEAF:
            return
        x0,z0,x1,z1 = self.rect
        h = (x1 - x0)/2
        rects = []
        rects.append((x0, z0, x0 + h, z0 + h))
        rects.append((x0, z0 + h, x0 + h, z1))
        rects.append((x0 + h, z0 + h, x1, z1))
        rects.append((x0 + h, z0, x1, z0 + h))
        for n in range(len(rects)):
            span = self.spans_feature(rects[n])
            if span == True:
                self.children[n] = self.getinstance(rects[n])
                self.children[n].subdivide()
   
    def contains(self, x, z):
        x0,z0,x1,z1 = self.rect
        if x >= x0 and x <= x1 and z >= z0 and z <= z1:
            return True
        return False
   
    def getinstance(self,rect):
        return Node(self,rect)            
    def spans_feature(self, rect):
        return False
  
           
class QuadTree():
    maxdepth = 1
    leaves = []
    allnodes = []
    
    def __init__(self, rootnode, minrect):
        Node.minsize = minrect
        rootnode.subdivide()
        self.prune(rootnode)
        self.traverse(rootnode)
    
    def prune(self, node):
        if node.type == Node.LEAF:
            return 1
        leafcount = 0
        removals = []
        for child in node.children:
            if child != None:
                leafcount += self.prune(child)
                if leafcount == 0:
                    removals.append(child)
        for item in removals:
            n = node.children.index(item)
            node.children[n] = None        
        return leafcount
    
    def traverse(self, node):
        QuadTree.allnodes.append(node)
        if node.type == Node.LEAF:
            QuadTree.leaves.append(node)
            if node.depth > QuadTree.maxdepth:
                QuadTree.maxdepth = node.depth
        for child in node.children:
            if child != None:
                self.traverse(child)