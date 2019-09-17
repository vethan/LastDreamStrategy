from itertools import chain

import Vector2Int
from TimelineObject import TimelineObject


class Unit(TimelineObject):
    def __init__(self,
                 name: str,
                 move: int,
                 speed: int,
                 team: int,
                 max_hp: int,
                 game,
                 start_position: Vector2Int):
        super().__init__(name, speed)
        self.move = move
        self.team = team
        self.game = game
        self.max_hp = max_hp
        self.hp = max_hp
        self.position = start_position.clone()
        self.action_taken = False
        self.move_used = False
        self.actions = []

    def __str__(self):
        return "Team " + str(self.team) + " " + self.name + "[" + str(self.hp) + "/" + str(self.max_hp) + "] " + str(
            self.position)

    def flatten(self, listOfLists):
        return list(chain.from_iterable(listOfLists))

    def get_possible_action_targets(self):
        return self.flatten([possible_actions.get_target_action_list() for possible_actions in self.actions])

    def move_to(self, new_position: Vector2Int.Vector2Int):
        if (self.CT < 100
                or self.move_used
                or not self.game.is_empty(new_position)
                or Vector2Int.Vector2Int.manhattan_distance(self.position, new_position) > self.move):
            return False

        self.position = new_position.clone()
        self.move_used = True
        return True

    def execute(self):
        self.game.handle_unit_action(self.team, self, self.game)

    def damage(self, amount):
        self.hp -= amount
        self.hp = max(min(self.max_hp, self.hp), 0)
        if self.hp <= 0:
            self.game.timeline_objects.remove(self)
            self.game.units.remove(self)

    def end_turn(self):
        if self.CT >= 100:
            if self.move_used and self.action_taken:
                self.CT = min(60, self.CT - 100)
            elif self.move_used or self.action_taken:
                self.CT = min(60, self.CT - 80)
            else:
                self.CT = min(60, self.CT - 60)
        else:
            super().end_turn()

        self.move_used = False
        self.action_taken = False
