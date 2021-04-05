from buildings.building import Building


class Wall(Building):
    UPGRADE_COSTS = [[25, 25, 25], [200, 200, 200], [800, 800, 800]]
    DEFENSE_BONUSES = [1, 1.1, 1.25, 1.5]

    def __init__(self):
        self.level = 0

    def defense_bonus(self):
        return self.DEFENSE_BONUSES[self.level]

    def next_defense_bonus(self):
        if self.is_max_level():
            return "(MAXED)"
        else:
            return self.DEFENSE_BONUSES[self.level + 1]
