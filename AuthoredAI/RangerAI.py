import AuthoredAI.CharacterAI
import Vector2Int
from Actions import BasicAttackAction


class RangerAI(AuthoredAI.CharacterAI.CharacterAI):
    def __init__(self, controlled_unit, game):
        super().__init__(controlled_unit, game)

    def decide_turn_action(self):
        ordered_enemies = self.get_enemies_by_distance()
        if len(ordered_enemies) == 0:
            return
        closest_enemy = ordered_enemies[0]
        # Move towards closest enemy
        distance = self.get_unit_distance(closest_enemy)
        if distance < self.unit.weapon.min_range:
            move_spaces = [x for x in self.get_unit_move_spaces() if
                           Vector2Int.Vector2Int.manhattan_distance(x, closest_enemy.position) >= self.unit.weapon.min_range]
            if len(move_spaces) > 0:
                self.unit.move_to(move_spaces[0])

        if distance > self.unit.weapon.max_range:
            move_spaces = [x for x in self.get_unit_move_spaces() if
                           Vector2Int.Vector2Int.manhattan_distance(x, closest_enemy.position) >= self.unit.weapon.min_range]
            options = len(move_spaces)
            if options == 1:
                self.unit.move_to(move_spaces[0])
            elif options > 0:
                # move to edge of attack range
                move_spaces.sort(key=lambda point: Vector2Int.Vector2Int.manhattan_distance(closest_enemy.position, point))
                min = Vector2Int.Vector2Int.manhattan_distance(closest_enemy.position, move_spaces[0])
                max = Vector2Int.Vector2Int.manhattan_distance(closest_enemy.position, move_spaces[options - 1])
                if min >= self.unit.weapon.max_range:
                    self.unit.move_to(move_spaces[0])
                elif max <= self.unit.weapon.max_range:
                    self.unit.move_to(move_spaces[options - 1])
                else:
                    for x in range(0, options):
                        if Vector2Int.Vector2Int.manhattan_distance(closest_enemy.position, move_spaces[x]) == self.unit.weapon.max_range:
                            self.unit.move_to(move_spaces[options - 1])
                            break


        if self.is_unit_in_weapon_range(closest_enemy):
            for action in self.unit.actions:
                if isinstance(action, BasicAttackAction.BasicAttackAction):
                    action.get_targeted_action(closest_enemy).select()
                    self.unit.action_taken = True
            return
