from buildings.building import Building


class Barracks(Building):

    def __init__(self):
        self.level = 0
        self.upgrade_costs = [50, 250, 750]
