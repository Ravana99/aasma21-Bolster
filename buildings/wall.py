from buildings.building import Building


class Wall(Building):

    def __init__(self):
        self.level = 0
        self.upgrade_costs = [25, 200, 800]
        self.defense_bonuses = [1, 1.1, 1.25, 1.5]

    def defense_bonus(self):
        return self.defense_bonuses[self.level]
