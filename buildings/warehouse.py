from buildings.building import Building


class Warehouse(Building):
    UPGRADE_COSTS = [None, 75, 150, 300, 600]
    CAPACITIES = [None, 100, 200, 400, 800, 1600]

    def __init__(self):
        self.level = 1

    def capacity(self):
        return self.CAPACITIES[self.level]

    def next_capacity(self):
        if self.is_max_level():
            return "(MAXED)"
        else:
            return self.CAPACITIES[self.level + 1]
