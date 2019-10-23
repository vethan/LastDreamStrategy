from itertools import chain

import Game
import Vector2Int
from TimelineObject import TimelineObject


class Unit(TimelineObject):
    def __init__(self,
                 name: str,
                 move: int,
                 speed: int,
                 eva: int,
                 faith: int,
                 p_attack: int,
                 m_attack: int,
                 team: int,
                 max_hp: int,
                 game: Game,
                 start_position: Vector2Int):
        super().__init__(name, speed)
        self.move = move
        self.team = team
        self.game = game
        self.char = "u"
        self.ai = None
        self.max_hp = max_hp
        self.evade = eva
        self.faith = faith
        self.p_attack = p_attack
        self.m_attack = m_attack
        self.hp = max_hp
        self.position = start_position.clone()
        self.action_taken = False
        self.move_used = False
        self.actions = []
        self.weapon = None
        self.debug_print = False

    def __str__(self):
        return self.name + "(" + self.char + ")" + "[" + str(self.hp) + "/" + str(
            self.max_hp) + "] " + str(
            Vector2Int.Vector2Int.to_battleship_coord(self.position))

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

        if self.debug_print:
            print(str(self) + " moved to "
                  + Vector2Int.Vector2Int.to_battleship_coord(new_position))

        self.position = new_position.clone()
        self.move_used = True
        return True

    def execute(self):
        self.game.handle_unit_action(self.team, self, self.game)

    def damage(self, amount):
        original_hp = self.hp
        self.hp -= amount
        self.hp = max(min(self.max_hp, self.hp), 0)
        actual_damage = original_hp - self.hp

        if self.debug_print:
            if actual_damage < 0:
                print(str(self) + " healed by " + str(-actual_damage))
            elif actual_damage > 0:
                print(str(self) + " damgaed by " + str(actual_damage))

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
