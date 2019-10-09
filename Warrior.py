import BasicAttackAction
import Unit
import Weapon
from Vector2Int import Vector2Int


# Based on a lvl 50 knight in FFT
# MOV=3, Jump=3, EVA=10, PA=16, MA=6, HP=279, SPD=8,

# Weapon: 5 so dmg = 5* 7 = 80

class Warrior(Unit.Unit):
    def __init__(self,
                 name: str,
                 team: int,
                 game,
                 start_position: Vector2Int,
                 char: str = 'w'):
        super().__init__(name=name,
                         speed=8,
                         move=3,
                         max_hp=279,
                         eva=10,
                         faith=55,
                         p_attack=16,
                         m_attack=6,
                         team=team,
                         game=game,
                         start_position=start_position)

        self.char = char
        self.defending = False
        self.action_taken = False
        self.move_used = False
        self.actions.append(BasicAttackAction.BasicAttackAction(weapon=Weapon.Sword(5,0), owner=self))
        self.actions.append(DefendAction(self))

    def defend(self):
        self.defending = True

    def execute(self):
        self.defending = False
        super().execute()

    def damage(self, amount: int):
        if self.defending and amount > 0:
            self.hp -= amount / 2
        else:
            self.hp -= amount

        self.hp = max(min(self.max_hp, self.hp), 0)
        if self.hp <= 0:
            self.game.timeline_objects.remove(self)
            self.game.units.remove(self)


class DefendAction:
    def __init__(self, owner):
        self.owner = owner

    def get_target_action_list(self):
        result = [DefendTarget(self, self.owner)]
        return result


class DefendTarget:
    def __init__(self, target, owner: Unit):
        self.target = target
        self.owner = owner

    def __str__(self):
        return "Defence Stance Team " + str(self.target.team) + " " + self.target.name

    def select(self):
        self.target.damage(self.owner.owner.defend())
