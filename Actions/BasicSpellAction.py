import Vector2Int
from TimelineObject import TimelineObject


class BasicSpellAction:
    def __init__(self, name: str, chargeTicks: int, max_range: int, power: int, owner):
        self.name = name
        self.chargeTicks = chargeTicks
        self.power = power
        self.owner = owner
        self.max_range = max_range

    def get_target_action_list(self):
        result = []
        for unit in self.owner.game.units:
            if (unit.team == self.owner.team
                    or Vector2Int.Vector2Int.manhattan_distance(unit.position, self.owner.position) > self.max_range):
                continue

            result.append(BasicSpellTarget(unit, self))

        return result


class HealingSpellAction:
    def __init__(self, name: str, chargeTicks: int, max_range: int, power: int, owner):
        self.name = name
        self.chargeTicks = chargeTicks
        self.power = -power
        self.owner = owner
        self.max_range = max_range

    def get_target_action_list(self):
        result = []
        for unit in self.owner.game.units:
            if (unit.team != self.owner.team
                    or Vector2Int.Vector2Int.manhattan_distance(unit.position, self.owner.position) > self.max_range):
                continue

            result.append(BasicSpellTarget(unit, self))

        return result


class BasicSpellTarget(TimelineObject):
    def __init__(self, target, owner):
        super().__init__(owner.owner.name + ": " + owner.name, 100 / owner.chargeTicks)
        self.target = target
        self.owner = owner

    def __str__(self):
        return self.owner.name + " Team " + str(self.target.team) + " " + self.target.name \
               + " for " + str(self.damage_calc()) + " damage"

    def damage_calc(self):
        return int(self.owner.owner.m_attack * self.owner.power * (self.owner.owner.faith * 0.01) * (
                    self.target.faith * 0.01))

    def select(self):
        self.owner.owner.game.timeline_objects.append(self)

    def execute(self):
        self.target.damage(self.damage_calc())


class AOESpellTarget(BasicSpellTarget):
    def __init__(self, target, owner, range):
        super().__init__(target, owner)
        self.target = target
        self.owner = owner
        self.range = range

    def execute(self):
        for unit in self.owner.game.units:
            if (Vector2Int.Vector2Int.manhattan_distance(self.target.position, self.owner.position) <= self.max_range):
                self.target.damage(self.damage_calc())
