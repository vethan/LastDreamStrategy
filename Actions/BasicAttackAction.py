import Vector2Int


class BasicAttackAction:
    def __init__(self, owner):
        self.owner = owner

    def get_targeted_action(self, target_unit):
        if (target_unit.team == self.owner.team
                or Vector2Int.Vector2Int.manhattan_distance(target_unit.position,
                                                            self.owner.position) > self.owner.weapon.max_range
                or Vector2Int.Vector2Int.manhattan_distance(target_unit.position,
                                                            self.owner.position) < self.owner.weapon.min_range):
            return None

        return BasicAttackTarget(target_unit, self)

    def get_target_action_list(self):
        result = []
        for unit in self.owner.game.units:
            if (unit.team == self.owner.team
                    or Vector2Int.Vector2Int.manhattan_distance(unit.position,
                                                                self.owner.position) > self.owner.weapon.max_range
                    or Vector2Int.Vector2Int.manhattan_distance(unit.position,
                                                                self.owner.position) < self.owner.weapon.min_range):
                continue

            result.append(BasicAttackTarget(unit, self))

        return result


class BasicAttackTarget:
    def __init__(self, target, owner: BasicAttackAction):
        self.target = target
        self.owner = owner

    def __str__(self):
        user = self.owner.owner
        damage = user.weapon.damage(user.m_attack, user.p_attack, user.speed)
        return "Basic attack Team " + str(self.target.team) + " " + self.target.name \
               + " for " + str(damage) + " damage"

    def select(self):
        # TODO: roll to hit
        user = self.owner.owner
        if user.debug_print:
            print(str(user) + " basic attacked " + str(self.target))
        self.target.damage(user.weapon.damage(user.m_attack, user.p_attack, user.speed))
