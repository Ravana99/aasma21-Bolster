from troops.troops import Troops


class Cavalrymen(Troops):
    ATTACK = 8
    DEFENSE = 8
    COST = [10, 10, 6]
    MIN_BARRACKS_LEVEL = 3
