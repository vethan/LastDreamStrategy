import Vector2Int


class BasicAttackAction:
    def __init__(self, max_range: int, damage: int, owner):
        self.damage = damage
        self.owner = owner
        self.max_range = max_range

    def get_target_action_list(self):
        result = []
        for unit in self.owner.game.units:
            if (unit.team == self.owner.team
                    or Vector2Int.Vector2Int.manhattan_distance(unit.position, self.owner.position) > self.max_range):
                continue

            result.append(BasicAttackTarget(unit, self))

        return result


class BasicAttackTarget:
    def __init__(self, target, owner: BasicAttackAction):
        self.target = target
        self.owner = owner

    def __str__(self):
        return "Basic attack Team " + str(self.target.team) + " " + self.target.name \
               + " for " + str(self.owner.damage) + " damage"

    def select(self):
        self.target.damage(self.owner.damage)
