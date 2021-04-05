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

    def upgrade(self, iron, stone, wood):
        if self.level >= len(self.UPGRADE_COSTS):
            raise UpgradeMaxedOutBuildingException()
        elif self.UPGRADE_COSTS[self.level][0] > iron or \
                self.UPGRADE_COSTS[self.level][1] > stone or \
                self.UPGRADE_COSTS[self.level][2] > wood:
            raise NotEnoughResourcesToUpgradeException()
        else:
            iron = iron - self.UPGRADE_COSTS[self.level][0]
            stone = stone - self.UPGRADE_COSTS[self.level][1]
            wood = wood - self.UPGRADE_COSTS[self.level][2]
            self.level += 1
            return iron, stone, wood
