from buildings.building import Building


class Warehouse(Building):
    UPGRADE_COSTS = [None, [75, 75, 75], [150, 150, 150], [300, 300, 300], [600, 600, 600]]
    CAPACITIES = [None, 200, 400, 800, 1600, 3200]

    def __init__(self):
        self.level = 1

    def capacity(self):
        return self.CAPACITIES[self.level]

    def next_capacity(self):
        if self.is_max_level():
            return "(MAXED)"
        else:
            return self.CAPACITIES[self.level + 1]
