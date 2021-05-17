from troops.warriors import Warriors
from troops.archers import Archers
from troops.catapults import Catapults
from troops.cavalrymen import Cavalrymen
from troops.report import Report
from random import uniform
from math import ceil, log
from troops.exceptions import AttackWithNoArmyException


class Army:
    def __init__(self, n_warriors, n_archers, n_catapults, n_cavalrymen,
                 village_name, attacking, enemy_village_name=""):
        n_warriors = int(n_warriors)
        n_archers = int(n_archers)
        n_catapults = int(n_catapults)
        n_cavalrymen = int(n_cavalrymen)
        if attacking and n_warriors + n_archers + n_catapults + n_cavalrymen <= 0:
            raise AttackWithNoArmyException()
        self.warriors = Warriors(n_warriors)
        self.archers = Archers(n_archers)
        self.catapults = Catapults(n_catapults)
        self.cavalrymen = Cavalrymen(n_cavalrymen)
        self.village_name = village_name
        self.attacking = attacking
        self.enemy_village_name = enemy_village_name

    def get_warriors(self):
        return self.warriors

    def get_archers(self):
        return self.archers

    def get_catapults(self):
        return self.catapults

    def get_cavalrymen(self):
        return self.cavalrymen

    def get_village_name(self):
        return self.village_name

    def get_enemy_village_name(self):
        return self.enemy_village_name

    def power(self):
        if self.attacking:
            return (self.warriors.get_attack_power() +
                    self.archers.get_attack_power() +
                    self.catapults.get_attack_power() +
                    self.cavalrymen.get_attack_power())
        else:
            return (self.warriors.get_defense_power() +
                    self.archers.get_defense_power() +
                    self.catapults.get_defense_power() +
                    self.cavalrymen.get_defense_power())

    def attack(self, defending_army, defense_bonus):
        # Generate random luck factors
        attacking_luck = uniform(0.8, 1.2)
        defending_luck = uniform(0.8, 1.2)

        # Compute powers (defending power must take into account the wall defense bonus of the village)
        attacking_power = self.power() * attacking_luck
        defending_power = defending_army.power() * defending_luck * defense_bonus

        # Whichever side has the most power wins
        winner = self if attacking_power >= defending_power else defending_army
        loser = defending_army if winner is self else self

        # Win magnitude, which will determine how many troops survive on the winning side, is based on power diff/ratio
        win_magnitude = (attacking_power - defending_power) / attacking_power if winner is self else \
            (defending_power - attacking_power) / defending_power

        # Determine how many troops on the winning side survive
        casualty_luck = uniform(2.0, 6.0)
        alpha = 2 ** casualty_luck
        survivor_ratio = log(1 + alpha * win_magnitude, 1 + alpha)

        # Start generating report
        report = Report(attacking_village=self.get_village_name(),
                        defending_village=defending_army.get_village_name(),
                        attacking_luck=attacking_luck,
                        defending_luck=defending_luck,
                        starting_attacking_warriors=self.get_warriors().get_n(),
                        starting_attacking_archers=self.get_archers().get_n(),
                        starting_attacking_catapults=self.get_catapults().get_n(),
                        starting_attacking_cavalrymen=self.get_cavalrymen().get_n(),
                        starting_defending_warriors=defending_army.get_warriors().get_n(),
                        starting_defending_archers=defending_army.get_archers().get_n(),
                        starting_defending_catapults=defending_army.get_catapults().get_n(),
                        starting_defending_cavalrymen=defending_army.get_cavalrymen().get_n(),
                        winner=winner.get_village_name(),
                        loser=loser.get_village_name(),
                        casualty_luck=casualty_luck,
                        attacking_power=attacking_power,
                        defending_power=defending_power)

        # Winning side has survivors, losing side gets wiped out
        winner.determine_survivors(survivor_ratio)
        loser.wipe_out()

        # If attackers win, set resources to plunder based on the total power of the surviving troops
        resources_to_plunder = self.power() if winner is self else 0

        # If attackers win, deal damage to the defending village based on the total power of the surviving troops
        damage_dealt = self.power() if winner is self else 0

        # Finish report
        report.set_ending_troops(ending_attacking_warriors=self.get_warriors().get_n(),
                                 ending_attacking_archers=self.get_archers().get_n(),
                                 ending_attacking_catapults=self.get_catapults().get_n(),
                                 ending_attacking_cavalrymen=self.get_cavalrymen().get_n(),
                                 ending_defending_warriors=defending_army.get_warriors().get_n(),
                                 ending_defending_archers=defending_army.get_archers().get_n(),
                                 ending_defending_catapults=defending_army.get_catapults().get_n(),
                                 ending_defending_cavalrymen=defending_army.get_cavalrymen().get_n())
        report.set_resources_to_plunder(resources_to_plunder)
        report.set_damage_dealt(damage_dealt)

        return report

    def wipe_out(self):
        self.determine_survivors(0)

    def determine_survivors(self, ratio):
        self.warriors.set_n(ceil(ratio * self.warriors.get_n()))
        self.archers.set_n(ceil(ratio * self.archers.get_n()))
        self.catapults.set_n(ceil(ratio * self.catapults.get_n()))
        self.cavalrymen.set_n(ceil(ratio * self.cavalrymen.get_n()))
