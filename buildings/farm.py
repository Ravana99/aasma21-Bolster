from buildings.building import Building


class Farm(Building):

    def __init__(self):
        self.level = 1
        self.upgrade_costs = [None, 80, 200, 500, 1250]
        self.capacities = [None, 10, 30, 90, 270, 810]

    def capacity(self):
        return self.capacities[self.level]
