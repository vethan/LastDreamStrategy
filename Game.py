import os
import random

from Unit import Warrior, Mage, Unit, Cleric
from Vector2Int import Vector2Int
from AuthoredAI.WarriorAI import WarriorAI


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


class Game:
    def __init__(self, map_width: int, map_height: int, handle_unit):
        self.map_width = map_width
        self.map_height = map_height
        self.timeline_objects = []
        self.units = []
        self.handle_unit_action = handle_unit
        self.running = True

    def add_unit(self, unit: Unit):
        self.timeline_objects.append(unit)
        self.units.append(unit)

    def advance(self):
        self.timeline_objects.sort(key=lambda timeline_object: timeline_object.steps_to_ready())
        to_be_removed = []
        for x in self.timeline_objects:
            x.end_turn()
            if x.CT >= 100:
                x.execute()
                if not isinstance(x, Unit.Unit):
                    to_be_removed.append(x)
                else:
                    x.end_turn()
        team1_unit = False
        team0_unit = False
        for unit in self.units:
            team0_unit |= unit.team == 0
            team1_unit |= unit.team == 1

        self.running = team0_unit and team1_unit

        for x in to_be_removed:
            self.timeline_objects.remove(x)

    def is_empty(self, position: Vector2Int):
        for x in self.units:
            if x.position == position:
                return False

        return True

    def turn_order_string(self):
        self.timeline_objects.sort(key=lambda timeline_object: timeline_object.steps_to_ready())
        return '\n'.join(str(x.CT) + " " + str(x) for x in self.timeline_objects)

    def roll_initiative(self):
        for unit in self.units:
            unit.CT = random.randint(0, 20)

    def draw_border(self):
        line = "-+"
        for i in range(0, self.map_width):
            line += "---+"

        print(line)

    def draw_grid(self):
        # draw header
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        line = " |"
        for i in range(0, self.map_width):
            line += " " + alphabet[i] + " |"
        print(line)
        self.draw_border()
        for y in range(0, self.map_height):
            line = str(y + 1) + "|"
            for x in range(0, self.map_width):
                unitHere = None
                for unit in self.units:
                    if unit.position == Vector2Int(x, y):
                        unitHere = unit
                if unitHere:
                    line += " " + unitHere.char + " |"
                else:
                    line += "   |"
            print(line)
            self.draw_border()


def handle_unit_move(unit: Unit):
    while True:
        print("Enter position co-ordinates or q to cancel")
        input_value = input()
        if input_value == 'q':
            return
        else:
            if Vector2Int.is_coordinate(input_value):
                position = Vector2Int.from_battleship_coord(input_value)
                if not unit.move_to(position):
                    print("Can't move there")
                else:
                    return
            else:
                print("Invalid coordinate")


def handle_unit_action(unit: Unit):
    while True:
        options = unit.get_possible_action_targets()
        if len(options) == 0:
            print("No actions available")
            return

        print("\n".join(str(index) + ". " + str(x) for index, x in enumerate(options)))

        print("Enter a choice or q to cancel")
        input_value = input()
        if input_value == 'q':
            return
        else:
            if input_value.isdigit():
                index = int(input_value)
                if index >= len(options):
                    print("Out of range")
                    continue

                options[index].select()
                unit.action_taken = True
                return
            else:
                print("Invalid entry")


def handle_unit_turn(team: int, unit: Unit, game: Game):
    if unit.ai is not None:
        unit.ai.decide_turn_action()
        return

    while True:
        print(unit.name + "(" + unit.char + ")" + " turn")
        if unit.action_taken and unit.move_used:
            return
        elif unit.move_used:
            input_value = input("1 for actions, 2 to wait")
            if input_value == "1":
                handle_unit_action(unit)
            elif input_value == "2":
                return
            return
        elif unit.action_taken:
            input_value = input("1 to move, 2 to wait")
            if input_value == "1":
                handle_unit_move(unit)
            elif input_value == "2":
                return
        else:
            input_value = input("1 to move, 2 for actions, 3 to wait")
            if input_value == "1":
                handle_unit_move(unit)
            elif input_value == "2":
                handle_unit_action(unit)
            elif input_value == "3":
                return


def main():
    game = Game(7, 7, handle_unit_turn)
    unit = Warrior.Warrior(name="Warrior 1", team=0, start_position=Vector2Int(1, 2), game=game, char='w')
    unit.ai = WarriorAI(unit, game)

    game.add_unit(unit)

    unit = Cleric.Cleric(name="Cleric 1", team=0, start_position=Vector2Int(0, 1), game=game, char='c')
    unit.ai = WarriorAI(unit, game)

    game.add_unit(unit)

    unit = Mage.Mage(name="Mage 1", team=0, start_position=Vector2Int(0, 0), game=game, char='m')
    unit.ai = WarriorAI(unit, game)

    game.add_unit(unit)

    unit = Warrior.Warrior(name="Warrior 2", team=1, start_position=Vector2Int.from_battleship_coord("g7"), game=game, char='W')
    unit.ai = WarriorAI(unit, game)
    game.add_unit(unit)

    unit = Cleric.Cleric(name="Cleric 2", team=1, start_position=Vector2Int(4, 2), game=game, char='C')
    unit.ai = WarriorAI(unit, game)

    game.add_unit(unit)

    unit = Mage.Mage(name="Mage 2", team=1, start_position=Vector2Int(4, 4), game=game, char='M')
    unit.ai = WarriorAI(unit, game)

    game.add_unit(unit)

    game.roll_initiative()

    while game.running:
        game.advance()
        cls()
        game.draw_grid()
        input(game.turn_order_string())


if __name__ == "__main__":
    main()
