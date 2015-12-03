from buffalo import utils
from npc import NPC
from enemy import Enemy
from friendly import Friendly
from trader import Trader

utils.init()
isWorking = False
enemy = Enemy(name="monster", fPos=(600.0,600.0))
friendly = Friendly(name="villager", fPos=(650.0,650.0))
trader = Trader(name="merchant", fPos=(800.0,800.0))
npcs = [enemy, friendly, trader]

for npc in npcs:
    NPC.load_sprites()
    NPC.move_X(4)
    NPC.move_Y(3)
    NPC.detectCollision(npcs)
    NPC.blit_sprite()
    
NPC.update()    
isWorking = True
assert isWorking