from buildings.building import Building


class Sawmill(Building):
    UPGRADE_COSTS = [None, [100, 100, 100], [250, 250, 250], [600, 600, 600], [1500, 1500, 1500]]
    PRODUCTIONS = [None, 5, 10, 20, 40, 80]

    def __init__(self):
        self.level = 1

    def production(self):
        return self.PRODUCTIONS[self.level]

    def next_production(self):
        if self.is_max_level():
            return "(MAXED)"
        else:
            return self.PRODUCTIONS[self.level + 1]
