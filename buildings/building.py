class Building:

    level = -1
    upgrade_costs = []

    def __init__(self):
        raise NotImplementedError()

    def get_level(self):
        return self.level

    def get_upgrade_costs(self):
        return self.upgrade_costs

    def upgrade(self, stone):
        if self.level >= len(self.upgrade_costs):
            raise Exception("Building already at max level")
        elif self.upgrade_costs[self.level] > stone:
            raise Exception("Not enough stone to upgrade building")
        else:
            stone = stone - self.upgrade_costs[self.level]
            self.level += 1
            return stone
