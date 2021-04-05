from buildings.building import Building


class Farm(Building):
    UPGRADE_COSTS = [None, [50, 50, 100], [125, 125, 250], [300, 300, 600], [750, 750, 1500]]
    CAPACITIES = [None, 10, 30, 90, 270, 810]

    def __init__(self):
        self.level = 1

    def capacity(self):
        return self.CAPACITIES[self.level]

    def next_capacity(self):
        if self.is_max_level():
            return "(MAXED)"
        else:
            return self.CAPACITIES[self.level + 1]
