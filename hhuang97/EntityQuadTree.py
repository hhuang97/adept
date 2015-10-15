"""
Combined Entity and Quadtree into same file, keep separate files in case useful
"""

#import quadTree
import pygame

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


def rect_quad_split(rect):
    w=rect.width/2.0
    h=rect.height/2.0
    rl=[]
    rl.append(pygame.Rect(rect.left, rect.top, w, h))
    rl.append(pygame.Rect(rect.left+w, rect.top, w, h))
    rl.append(pygame.Rect(rect.left, rect.top+h, w, h))
    rl.append(pygame.Rect(rect.left+w, rect.top+h, w, h))
    return rl

def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
displayTree = False

class Quadtree(object):
    def __init__(self, level, rect, particles=[], color = (0,0,0)):
        self.maxlevel = 4#max number of subdivisions
        self.level = level#current level of subdivision
        self.maxparticles = 3#max number of particles without subdivision
        self.rect = rect#pygame rect object
        self.particles = particles#list of particles
        self.color = color#color of box if displayed
        self.branches = []#empty list that is filled with four branches if subdivided

    def get_rect(self):
        return self.rect

    def subdivide(self):
        for rect in rect_quad_split(self.rect):
            branch = Quadtree(self.level+1, rect, [], (self.color[0]+30,self.color[1],self.color[2]))
            self.branches.append(branch)

    def add_particle(self, particle):
        self.particles.append(particle)

    def subdivide_particles(self):
        for particle in self.particles:
            for branch in self.branches:
                if branch.get_rect().colliderect(particle.get_rect()):
                    branch.add_particle(particle)

    def render(self, display):
        pygame.draw.rect(display, self.color, self.rect)

    def test_collisions(self):
        for i, particle in enumerate(self.particles):
            for particle2 in self.particles[i+1:]:
                collide(particle, particle2)
            
    def update(self, display):
        if len(self.particles) > self.maxparticles and self.level <= self.maxlevel:
            self.subdivide()
            self.subdivide_particles()
            for branch in self.branches:
                branch.update(display)
        else:
            self.test_collisions()
            if displayTree:
                self.render(display)