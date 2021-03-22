from buildings.exceptions import *


class Building:
    UPGRADE_COSTS = []

    level = -1

    def __init__(self):
        raise NotImplementedError()

    def get_level(self):
        return self.level

    def get_max_level(self):
        return len(self.UPGRADE_COSTS)

    def is_max_level(self):
        return self.level == self.get_max_level()

    def get_upgrade_costs(self):
        return self.UPGRADE_COSTS

    def get_cost_of_upgrade(self):
        return self.UPGRADE_COSTS[self.level]

    def upgrade(self, stone):
        if self.level >= len(self.UPGRADE_COSTS):
            raise UpgradeMaxedOutBuildingException()
        elif self.UPGRADE_COSTS[self.level] > stone:
            raise NotEnoughStoneToUpgradeException()
        else:
            stone = stone - self.UPGRADE_COSTS[self.level]
            self.level += 1
            return stone
