from buildings.building import Building


class Barracks(Building):
    UPGRADE_COSTS = [50, 250, 750]

    def __init__(self):
        self.level = 0
