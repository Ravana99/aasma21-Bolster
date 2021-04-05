from troops.warriors import Warriors
from troops.archers import Archers
from troops.catapults import Catapults
from random import uniform
from math import ceil, log
from troops.exceptions import AttackWithNoArmyException


class Army:
    def __init__(self, n_warriors, n_archers, n_catapults, village_name, attacking, enemy_village_name=""):
        n_warriors = int(n_warriors)
        n_archers = int(n_archers)
        n_catapults = int(n_catapults)
        if attacking and n_warriors + n_archers + n_catapults <= 0:
            raise AttackWithNoArmyException()
        self.warriors = Warriors(n_warriors)
        self.archers = Archers(n_archers)
        self.catapults = Catapults(n_catapults)
        self.village_name = village_name
        self.attacking = attacking
        self.enemy_village_name = enemy_village_name

    def get_warriors(self):
        return self.warriors

    def get_archers(self):
        return self.archers

    def get_catapults(self):
        return self.catapults

    def get_village_name(self):
        return self.village_name

    def get_enemy_village_name(self):
        return self.enemy_village_name

    def power(self):
        if self.attacking:
            return (self.warriors.get_attack_power() +
                    self.archers.get_attack_power() +
                    self.catapults.get_attack_power())
        else:
            return (self.warriors.get_defense_power() +
                    self.archers.get_defense_power() +
                    self.catapults.get_defense_power())

    def attack(self, defending_army, defense_bonus):
        attacking_luck = uniform(0.8, 1.2)
        defending_luck = uniform(0.8, 1.2)
        attacking_power = self.power() * attacking_luck
        defending_power = defending_army.power() * defending_luck * defense_bonus

        winner = self if attacking_power >= defending_power else defending_army
        loser = defending_army if winner is self else self

        win_magnitude = (attacking_power - defending_power) / attacking_power if winner is self else \
            (defending_power - attacking_power) / defending_power

        casualty_luck = uniform(2.0, 6.0)
        alpha = 2 ** casualty_luck
        survivor_ratio = log(1 + alpha * win_magnitude, 1 + alpha)

        winner.determine_survivors(survivor_ratio)
        loser.wipe_out()

        return self.power() if winner is self else 0

    def wipe_out(self):
        self.determine_survivors(0)

    def determine_survivors(self, ratio):
        self.warriors.set_n(ceil(ratio * self.warriors.get_n()))
        self.archers.set_n(ceil(ratio * self.archers.get_n()))
        self.catapults.set_n(ceil(ratio * self.catapults.get_n()))
