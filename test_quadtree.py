import entityManager
from entity import Entity
import random, time

class Test:
    idCounter = 0
    
    def __init__(self, x, y):
        Entity.x = x
        Entity.y = y
        left = Entity.x-1
        right = Entity.x+1
        top = Entity.y-1
        bottom = Entity.y+1
        self.boundary_box = [left,top,right,bottom]
        Test.idCounter+=1
        self.id = Test.idCounter

    def __str__(self):
        return "entity " + (str)(self.id)

isWorking = False
# tests with x random entities with coordinates 1-10 in x and y directions
x = 1000
entities = [Test(random.randrange(1,10),random.randrange(1,10)) for _ in range(x)]
index = entityManager.Manager(boundary_box=[-11,-33,100,100])
t_i = time.time()
for entity in entities:
    index.insert(entity, entity.boundary_box)
#     print entity # print memory address of each Entity object

t_e = time.time()
if t_e-t_i > 10:
    assert isWorking
    
print "inserting ",x," entities: ",(t_e - t_i)," seconds"

print "test collisions with ",x," entities"
test_entity = (5, 5, 5, 5)
t_start = time.time()
matches = index.intersect(test_entity) # list of all entities at 5, 5
t_end = time.time()
print "runtime: ",t_end - t_start," seconds"
print map(str, matches)
isWorking = True
assert isWorking
