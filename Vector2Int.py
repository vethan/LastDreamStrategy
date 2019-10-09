class Vector2Int:
    def __init__(self,
                 x: int,
                 y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __eq__(self, obj):
        return isinstance(obj, Vector2Int) and obj.x == self.x and obj.y == self.y

    def clone(self):
        return Vector2Int(self.x, self.y)

    @classmethod
    def from_battleship_coord(cls, input_value: str):
        alpha_section = input_value[0]
        digit_section = input_value[1:]
        x = ord(alpha_section) - 96
        y = int(digit_section)
        return Vector2Int(x-1, y-1)

    @classmethod
    def to_battleship_coord(cls, input_value):
        alpha = "abcdefghijklmnopqrstuvwxyz"
        coord = alpha[input_value.x]
        coord += str(input_value.y+1)
        return coord

    @classmethod
    def is_coordinate(cls, input_value: str):
        if len(input_value) < 2:
            return False
        alpha_section = input_value[0]
        digit_section = input_value[1:]
        if alpha_section.isalpha() and digit_section.isdigit():
            return True
        else:
            return False

    @classmethod
    def manhattan_distance(cls, position, new_position):
        return abs(position.x-new_position.x) + abs(position.y-new_position.y)
