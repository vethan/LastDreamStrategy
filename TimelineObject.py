from math import ceil


class TimelineObject:
    def __init__(self,name: str, speed: float):
        self.speed = speed
        self.CT = 0
        self.name = name

    def execute(self):
        pass

    def end_turn(self):
        self.CT += self.speed

    def is_ready(self):
        return self.CT >= 100

    def steps_to_ready(self):
        return (100.0-self.CT)/self.speed