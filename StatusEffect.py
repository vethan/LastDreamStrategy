from DamageType import DamageType


class StatusEffect():
    def __init__(self):
        pass;

    def OnTurnStart(self):
        pass;

    def AdjustDamageTaken(self, damageTaken: int, damageType: DamageType):
        pass;


    def AdjustDamageGiven(self):
        pass;