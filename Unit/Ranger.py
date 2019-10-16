from Actions import BasicSpellAction, BasicAttackAction
from Unit import Unit
import Weapon
from Vector2Int import Vector2Int


# Based on a lvl 50 archer in FFT
# MOV=3, Jump=3, EVA=10, PA=12, MA=5, HP=169, SPD=9, Faith=55

# Weapon: 5 so dmg = 5 * (12+9)/2 = 50

class Ranger(Unit.Unit):
    def __init__(self,
                 name: str,
                 team: int,
                 game,
                 start_position: Vector2Int,
                 char: str = 'r'):
        super().__init__(name=name,
                         speed=9,
                         move=3,
                         max_hp=169,
                         eva=10,
                         faith=55,
                         p_attack=12,
                         m_attack=5,
                         team=team,
                         game=game,
                         start_position=start_position)

        self.char = char
        self.action_taken = False
        self.move_used = False
        self.weapon = Weapon.Bow(5)
        self.actions.append(BasicAttackAction.BasicAttackAction(owner=self))
        self.actions.append(BasicSpellAction.BasicSpellAction(damage=65, max_range=3, chargeTicks=6, owner=self,
                                                              name="Charged Shot"))
