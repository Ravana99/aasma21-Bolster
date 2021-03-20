from buildings.building import Building


class Warehouse(Building):

    def __init__(self):
        self.level = 1
        self.upgrade_costs = [None, 75, 150, 300, 600]
        self.capacities = [None, 100, 200, 400, 800, 1600]

    def capacity(self):
        return self.capacities[self.level]
