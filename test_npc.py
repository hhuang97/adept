from buffalo import utils
from npc import NPC
from enemy import Enemy
from friendly import Friendly

utils.init()
isWorking = False
A = NPC.__init__(Enemy, 3, 10, 1)
B = NPC.__init__(Friendly, 2, 25, 3)
npcs = [A, B]

for npc in npcs:
    NPC.load_sprites()
    A.move("d")
    B.move("r")
    NPC.detectCollision(npcs)
    NPC.blit_sprite()
    
NPC.update()    
isWorking = True
assert isWorking