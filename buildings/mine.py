from buildings.building import Building


class Mine(Building):

    def __init__(self):
        self.level = 1
        self.upgrade_costs = [None, 100, 250, 600, 1500]
        self.productions = [0, 5, 10, 20, 40, 80]

    def production(self):
        return
