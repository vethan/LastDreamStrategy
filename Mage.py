import BasicAttackAction
import BasicSpellAction
import Unit
import Weapon
from Vector2Int import Vector2Int
from BasicSpellAction import BasicSpellAction
from BasicAttackAction import BasicAttackAction

# Based on a lvl 50 black mage in FFT
# MOV=3, Jump=3, EVA=,5 PA=4, MA=16, HP=112, SPD=8, Faith=70


# Weapon: 3 so dmg = 3* 4 = 8
#Black magic: Power = 6*16 * 0.8 = 77
class Mage(Unit.Unit):
    def __init__(self,
                 name: str,
                 team: int,
                 game,
                 start_position: Vector2Int,
                 char: str = 'm'):
        super().__init__(name=name,
                         speed=8,
                         move=3,
                         max_hp=112,
                         eva=5,
                         faith=70,
                         p_attack=4,
                         m_attack=16,
                         team=team,
                         game=game,
                         start_position=start_position)
        self.char = char
        self.action_taken = False
        self.move_used = False
        self.actions.append(BasicAttackAction(weapon=Weapon.Rod(3), owner=self))
        self.actions.append(BasicSpellAction(power=6, max_range=4, chargeTicks=4, owner=self, name="Magic Missiles"))
