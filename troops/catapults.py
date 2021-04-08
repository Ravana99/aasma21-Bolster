from troops.troops import Troops


class Catapults(Troops):
    ATTACK = 7
    DEFENSE = 2
    COST = [2, 2, 8]
    MIN_BARRACKS_LEVEL = 2
