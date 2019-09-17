import BasicAttackAction
import BasicSpellAction
import Unit
from Vector2Int import Vector2Int
from BasicSpellAction import BasicSpellAction
from BasicAttackAction import BasicAttackAction

# Based on a lvl 50 black mage in FFT
# MOV=3, Jump=3, EVA=,5 PA=4, MA=16, HP=112, SPD=8


# Weapon: 3 so dmg = 3* 4 = 8
#Black magic: Power = 6*16 * 0.8 = 77
class Mage(Unit.Unit):
    def __init__(self,
                 name: str,
                 team: int,
                 game,
                 start_position: Vector2Int):
        super().__init__(name=name,
                         speed=8,
                         move=3,
                         max_hp=112,
                         team=team,
                         game=game,
                         start_position=start_position)

        self.action_taken = False
        self.move_used = False
        self.actions.append(BasicAttackAction(damage=8, max_range=1, owner=self))
        self.actions.append(BasicSpellAction(damage=77, max_range=4, chargeTicks=4, owner=self, name="Magic Missiles"))
