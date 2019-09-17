from BasicAttackAction import BasicAttackAction
from BasicSpellAction import HealingSpellAction
from Game import Game
from Unit import Unit
from Vector2Int import Vector2Int


# Based on a lvl 50 white mage in FFT
# MOV=3, Jump=3, EVA=,5 PA=7, MA=14, HP=134, SPD=9

# Weapon: 3 so dmg = 3* 14 = 42 (Staves use magic attack)

#Cure: 6*14*.8 = 67.2
class Cleric(Unit):
    def __init__(self,
                 name: str,
                 team: int,
                 game: Game,
                 start_position: Vector2Int):
        super().__init__(name=name,
                         speed=9,
                         move=3,
                         max_hp=134,
                         team=team,
                         game=game,
                         start_position=start_position)

        self.action_taken = False
        self.move_used = False
        self.actions.append(BasicAttackAction(damage=42, max_range=1, owner=self))
        self.actions.append(
            HealingSpellAction(damage=67, max_range=3, chargeTicks=3, owner=self, name="Heal"))
