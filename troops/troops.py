from troops.exceptions import *


class Troops:
    """DO NOT INSTANTIATE!"""

    ATTACK = -1
    DEFENSE = -1
    COST = [-1, -1, -1]
    MIN_BARRACKS_LEVEL = -1

    def __init__(self, n=0):
        self.n = n

    def get_n(self):
        return self.n

    def set_n(self, n):
        self.n = n

    def get_attack_power(self):
        return self.n * self.ATTACK

    def get_defense_power(self):
        return self.n * self.DEFENSE

    def recruit(self, iron, stone, wood, n, level, free_capacity):
        if not (isinstance(n, int) or n.isdigit()):
            raise InvalidTroopsToRecruitException()
        else:
            n = int(n)
            if n < 0:
                raise InvalidTroopsToRecruitException()
            if level < self.MIN_BARRACKS_LEVEL:
                raise BarracksLevelTooLowException()
            elif n > free_capacity:
                raise NotEnoughFarmCapacityException()
            elif self.COST[0] * n > iron or \
                    self.COST[1] * n > stone or \
                    self.COST[2] * n > wood:
                raise NotEnoughResourcesToRecruitException()
            else:
                iron = iron - self.COST[0] * n
                stone = stone - self.COST[1] * n
                wood = wood - self.COST[2] * n
                self.n += n
                return iron, stone, wood

    def demote(self, n):
        if not (isinstance(n, int) or n.isdigit()):
            raise InvalidTroopsToDemoteException()
        else:
            n = int(n)
            if n < 0:
                raise InvalidTroopsToDemoteException()
            elif n > self.n:
                raise TooManyTroopsToDemoteException()
            else:
                self.n -= n

    def send_off(self, n):
        if not (isinstance(n, int) or n.isdigit()):
            raise InvalidTroopsToSendOffException()
        else:
            n = int(n)
            if n < 0:
                raise InvalidTroopsToSendOffException()
            elif n > self.n:
                raise InvalidTroopsToSendOffException()
            else:
                self.n -= n
