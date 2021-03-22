from troops.exceptions import *


class Troops:
    ATTACK = -1
    DEFENSE = -1
    COST = -1
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

    def recruit(self, stone, n, level, free_capacity):
        if not n.isdigit():
            raise InvalidTroopsToRecruitException()
        else:
            n = int(n)
            if n < 0:
                raise InvalidTroopsToRecruitException()
            if level < self.MIN_BARRACKS_LEVEL:
                raise BarracksLevelTooLowException()
            elif n > free_capacity:
                raise NotEnoughFarmCapacityException()
            elif self.COST * n > stone:
                raise NotEnoughStoneToRecruitException()
            else:
                stone = stone - self.COST * n
                self.n += n
                return stone

    def demote(self, n):
        if not n.isdigit():
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
        if not n.isdigit():
            raise InvalidTroopsToSendOffException()
        else:
            n = int(n)
            if n < 0:
                raise InvalidTroopsToSendOffException()
            elif n > self.n:
                raise TooManyTroopsToSendOffException()
            else:
                self.n -= n
