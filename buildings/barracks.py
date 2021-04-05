from buildings.building import Building


class Barracks(Building):
    UPGRADE_COSTS = [[50, 50, 50], [250, 250, 250], [750, 750, 750]]

    def __init__(self):
        self.level = 0
