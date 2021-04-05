from troops.troops import Troops


class Catapults(Troops):
    ATTACK = 10
    DEFENSE = 3
    COST = [10, 10, 10]
    MIN_BARRACKS_LEVEL = 3
