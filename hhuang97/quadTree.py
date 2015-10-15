class Node():
    ROOT = 0
    BRANCH = 1
    LEAF = 2
    minsize = 1
    
    def __init__(self, parent, rect):
        self.parent = parent
        self.children = [None, None, None, None]
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
   
    def optimize(self, limit_aspect=True):
        all = self.list_nodes()
        all.sort(key=lambda x:x[1].y)
        all.sort(key=lambda x:x[1].x)
        changed = True
        for i in range(2):
            while changed:
                changed = False
                for i, (parent_one, one) in enumerate(all):
                    try:
                        parent_two, two = all[i+1]
                    except IndexError:
                        break
                    if one.bottomleft == two.bottomright and one.height == two.height:
                        if limit_aspect and two.width > 2 * two.height:
                            continue
                        parent_one.remove(one)
                        del all[i]
                        two.width += one.width
                    elif two.topleft == one.bottomleft and one.width == two.width:
                        if limit_aspect and two.height > 2 * two.width:
                            continue
                        parent_one.remove(one)
                        del all[i]
                        two.height += one.height
                    elif two.bottomleft == one.bottomright and one.height == two.height:
                        if limit_aspect and one.width > 2 * one.height:
                            continue
                        parent_two.remove(two)
                        del all[i+1]
                        one.width += two.width
                    elif one.topleft == two.bottomleft and one.width == two.width:
                        if limit_aspect and one.height > 2 * one.width:
                            continue
                        parent_two.remove(two)
                        del all[i+1]
                        one.height += two.height
                    else:
                        continue
                    changed = True
                    break
            all.sort(key=lambda x:x[1].x)
            all.sort(key=lambda x:x[1].y)
            changed = True
   
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
                
    def find_neighbors(self):
        all = self.list_nodes()
        for op, one in all:
            for tp, two in all:
                if one is two: continue
                if one.left == two.right and (one.bottom < two.top and one.top > two.bottom):
                    one.n_left.append(two)
                elif one.right == two.left and (one.bottom < two.top and one.top > two.bottom):
                    one.n_right.append(two)
                elif one.top == two.bottom and (one.left < two.right and one.right > two.left):
                    one.n_top.append(two)
                elif one.bottom == two.top and (one.left < two.right and one.right > two.left):
                    one.n_bottom.append(two)