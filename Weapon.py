class Weapon:
    def __init__(self, attack: int, defence: int, magic: int, min_range=1, max_range=1):
        self.attack = attack
        self.defence = defence
        self.magic = magic
        self.min_range = min_range
        self.max_range = max_range

    def damage(self, physical_attack: int, magic_attack: int, speed: int) -> int:
        return self.attack

    def get_min_range(self):
        return self.min_range

    def get_max_range(self):
        return self.max_range


class Bow(Weapon):
    def __init__(self, attack: int):
        super().__init__(attack, 0, 0, min_range=3, max_range=5)

    def damage(self, physical_attack: int, magic_attack: int, speed: int) -> int:
        return ((physical_attack + speed) / 2) * self.attack


class Sword(Weapon):
    def __init__(self, attack: int, defence: int):
        super().__init__(attack, defence, 0)

    def damage(self, physical_attack: int, magic_attack: int, speed: int) -> int:
        return physical_attack * self.attack


class Staff(Weapon):
    def __init__(self, attack: int):
        super().__init__(attack, 15, 0)

    def damage(self, physical_attack: int, magic_attack: int, speed: int) -> int:
        return magic_attack * self.attack


class Rod(Weapon):
    def __init__(self, attack: int):
        super().__init__(attack, 20, 0)

    def damage(self, physical_attack: int, magic_attack: int, speed: int) -> int:
        return physical_attack * self.attack
