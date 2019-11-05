from Actions import BasicAttackAction
import AuthoredAI.CharacterAI


class WarriorAI(AuthoredAI.CharacterAI.CharacterAI):
    def __init__(self, controlled_unit, game):
        super().__init__(controlled_unit, game)

    def decide_turn_action(self):
        ordered_enemies = self.get_enemies_in_moveable_attack_range(self.unit.weapon.min_range,
                                                                    self.unit.weapon.max_range)
        if len(ordered_enemies) == 0:
            ordered_enemies = self.get_enemies_by_distance()
            if len(ordered_enemies) == 0:
                return

        closest_enemy = ordered_enemies[0]
        # Move towards closest enemy
        self.move_towards_unit(closest_enemy, self.unit.move)

        if self.is_unit_in_weapon_range(closest_enemy):
            for action in self.unit.actions:
                if isinstance(action, BasicAttackAction.BasicAttackAction):
                    action.get_targeted_action(closest_enemy).select()
                    self.unit.action_taken = True
            return
