from troops.troops import Troops


class Catapults(Troops):
    attack = 10
    defense = 3
    cost = 10
    min_level = 3

    def __init__(self):
        pass
