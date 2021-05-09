from buildings.building import Building


class Mine(Building):
    UPGRADE_COSTS = [None, [50, 90, 90], [125, 200, 200], [300, 500, 500], [750, 1250, 1250]]
    PRODUCTIONS = [None, 20, 40, 80, 160, 320]

    def __init__(self):
        self.level = 1

    def production(self):
        return self.PRODUCTIONS[self.level]

    def next_production(self):
        if self.is_max_level():
            return "(MAXED)"
        else:
            return self.PRODUCTIONS[self.level + 1]
