from buildings.building import Building


class Barracks(Building):
    UPGRADE_COSTS = [[60, 60, 30], [300, 300, 150], [900, 900, 450]]

    def __init__(self):
        self.level = 0
