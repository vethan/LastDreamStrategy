from Vector2Int import Vector2Int


class CharacterAI:
    def __init__(self, controlled_unit, game):
        self.unit = controlled_unit
        self.game = game

    def get_unit_distance(self, unit):
        return Vector2Int.manhattan_distance(self.unit.position, unit.position)

    def is_unit_in_weapon_range(self, unit):
        distance = self.get_unit_distance(unit)
        return self.unit.weapon.max_range >= distance >= self.unit.weapon.min_range

    def get_unit_move_spaces(self, limit=None):
        result = []
        move_range = self.unit.move
        if limit is not None:
            move_range = limit
        for x in range(-move_range, move_range):
            for y in range(-move_range, move_range):
                new_position = Vector2Int(self.unit.position.x + x, self.unit.position.y + y)
                if abs(x) + abs(y) <= move_range and (abs(x) > 0 or abs(y) > 0) and self.game.is_empty(new_position):
                    result.append(new_position)

        return result

    def get_enemies_by_distance(self):
        unit_list = []
        for unit in self.game.units:
            if unit.team == self.unit.team:
                continue
            unit_list.append(unit)

        unit_list.sort(key=self.get_unit_distance)
        return unit_list

    def move_towards_unit(self, unit, move):
        if self.get_unit_distance(unit) == 1 or move == 0:
            return

        available_spaces = self.get_unit_move_spaces(move)
        available_spaces.sort(key=lambda point: Vector2Int.manhattan_distance(unit.position, point))
        # First attempt to move to adjacent spots
        self.unit.move_to(available_spaces[0])

        # Move as close as possible