from enum import Enum


class Stance(Enum):
    NEUTRAL = 0
    OFFENSIVE = 1
    DEFENSIVE = 2

    # Helps decide whether or not to attack based on recent losses (number of turns to wait)
    def get_recovery_turns(self):
        if self == Stance.NEUTRAL:
            return 5
        elif self == Stance.OFFENSIVE:
            return 3
        else:
            return 10

    # Amount of most recent turns that agents can formulate their beliefs based on (reports, espionages...)
    def get_last_turns(self):
        if self == Stance.NEUTRAL:
            return 5
        elif self == Stance.OFFENSIVE:
            return 10
        else:
            return 3

    # self.attack_power / other.defense_power ratio required to send an attack
    def get_magnitude(self):
        if self == Stance.NEUTRAL:
            return 1.1
        elif self == Stance.OFFENSIVE:
            return 1
        else:
            return 2.5

    # Which function to call to determine total attack power (namely, whether or not to include defensive troops)
    def get_attack_power(self, agent):
        if self == Stance.NEUTRAL:
            return agent.village.get_attack_power_no_archers()
        elif self == Stance.OFFENSIVE:
            return agent.village.get_attack_power()
        else:
            return agent.village.get_attack_power_no_archers()

    # How many turns to wait without attacking/defending in order to upgrade its stance's offensiveness
    def get_turns_without_fighting(self):
        if self == Stance.NEUTRAL:
            return 50
        elif self == Stance.OFFENSIVE:
            raise Exception("Should not get here! Check code that calls stance.get_turns_without_fighting()")
        else:
            return 25

    # Fraction of village warriors to send out on attacks
    def get_warrior_send_ratio(self):
        if self == Stance.NEUTRAL:
            return 1
        elif self == Stance.OFFENSIVE:
            return 1
        else:
            return 0.5

    # Fraction of village archers to send out on attacks
    def get_archer_send_ratio(self):
        if self == Stance.NEUTRAL:
            return 0
        elif self == Stance.OFFENSIVE:
            return 1
        else:
            return 0

    # Fraction of village catapults to send out on attacks
    def get_catapult_send_ratio(self):
        if self == Stance.NEUTRAL:
            return 1
        elif self == Stance.OFFENSIVE:
            return 1
        else:
            return 1

    # Fraction of village cavalrymen to send out on attacks
    def get_cavalrymen_send_ratio(self):
        if self == Stance.NEUTRAL:
            return 1
        elif self == Stance.OFFENSIVE:
            return 1
        else:
            return 0.5
