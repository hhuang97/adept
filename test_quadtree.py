import entityManager
from entity import Entity
import random, time

# tests with x random entities with random  x and y coordinates 1-10
isWorking = False
x = 1000
entities = [Entity(random.randrange(1,10),random.randrange(1,10)) for _ in range(x)]
index = entityManager.Manager(boundary_box=[1,1,32,32])
t_i = time.time()
for entity in entities:
    index.insert(entity, entity.boundary_box)
t_e = time.time()
if t_e-t_i > 10:
    assert isWorking
print "inserting ",x," entities: ",(t_e - t_i)," seconds"

print "test collisions with ",x," entities"
test_entity = (3, 3, 5, 5)
t_start = time.time()
matches = index.intersect(test_entity) # list of all entities between (4,4) and (5,5)
t_end = time.time()
print "runtime: ",t_end - t_start," seconds"
print map(str, matches)
isWorking = True
assert isWorking
