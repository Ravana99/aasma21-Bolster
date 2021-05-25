import random
from agent.agent import Agent
from agent.decisions import *
from agent.stance import Stance
from math import ceil


class ReactiveAgent(Agent):

    def __init__(self, i, stance):
        super().__init__(i)

        # Starting stance (neutral, offensive or defensive)
        self.stance = stance

        # Fraction of resources that the agent is willing to spend on troops in a single recruit decision
        self.troop_focus = random.uniform(0.3, 0.7)

        # Stance history throughout the game
        self.stance_history = [(self.stance, 0)]

        # Attack power over the last 10 turns
        self.previous_attack_powers = [0] * 10

        self.possible_upgrade_decisions = []
        self.possible_recruit_decisions = []
        self.possible_spying_decisions = []
        self.possible_attack_decisions = []
        self.turns_since_last_attack = 0
        self.turns_since_last_defense = 0
        self.turns_since_last_attack_loss = 0
        self.turns_since_last_defense_loss = 0

    # UPGRADE DECISION

    def upgrade_decision(self):
        # New turn - update state/beliefs
        self.update_state()
        self.change_stance()

        self.possible_upgrade_decisions = self.upgrade_options()
        action = self.upgrade_filter()
        assert issubclass(action.__class__, UpgradeDecision)
        return action.execute()

    def upgrade_options(self):
        options = []
        for building in self.village.get_all_buildings():
            if self.can_upgrade(building):
                options.append(self.building_to_upgrade_action(building))
        options.append(UpgradeNothingDecision(self))
        return options

    def upgrade_filter(self):
        # Priority system as follows:
        # - Upgrade farm if farm is full
        # - Upgrade warehouse if production of a resource is > 0.5 * warehouse capacity
        # - Upgrade barracks
        # - Upgrade wall if agent is defensive
        # - Upgrade resource camp, prioritizing resource with lowest amount
        # - Upgrade wall if agent is not defensive
        # - Upgrade warehouse if full of at least one resource
        # - Upgrade farm if warehouse is full (just as a resource dump)
        # - Upgrade nothing

        decisions = []

        # Farm
        if self.village.get_troops() == self.get_farm().capacity():
            decisions.append(self.choose(self.possible_upgrade_decisions, UpgradeFarmDecision))

        # Warehouse (if producing a lot)
        if self.village.get_mine().production() > 0.5 * self.village.get_warehouse().capacity() or \
           self.village.get_quarry().production() > 0.5 * self.village.get_warehouse().capacity() or \
           self.village.get_sawmill().production() > 0.5 * self.village.get_warehouse().capacity():
            decisions.append(self.choose(self.possible_upgrade_decisions, UpgradeWarehouseDecision))

        # Barracks
        decisions.append(self.choose(self.possible_upgrade_decisions, UpgradeBarracksDecision))

        # Wall (if defensive)
        if self.stance == Stance.DEFENSIVE:
            decisions.append(self.choose(self.possible_upgrade_decisions, UpgradeWallDecision))

        # Resource camp
        if self.village.get_iron() >= self.village.get_stone() >= self.village.get_wood():
            priorities = [UpgradeMineDecision(self), UpgradeQuarryDecision(self), UpgradeSawmillDecision(self)]
        elif self.village.get_iron() >= self.village.get_wood() >= self.village.get_stone():
            priorities = [UpgradeMineDecision(self), UpgradeSawmillDecision(self), UpgradeQuarryDecision(self)]
        elif self.village.get_stone() >= self.village.get_iron() >= self.village.get_wood():
            priorities = [UpgradeQuarryDecision(self), UpgradeMineDecision(self), UpgradeSawmillDecision(self)]
        elif self.village.get_stone() >= self.village.get_wood() >= self.village.get_iron():
            priorities = [UpgradeQuarryDecision(self), UpgradeSawmillDecision(self), UpgradeMineDecision(self)]
        elif self.village.get_wood() >= self.village.get_iron() >= self.village.get_stone():
            priorities = [UpgradeSawmillDecision(self), UpgradeMineDecision(self), UpgradeQuarryDecision(self)]
        else:
            priorities = [UpgradeSawmillDecision(self), UpgradeQuarryDecision(self), UpgradeMineDecision(self)]
        for i in range(3):
            decisions.append(self.choose(self.possible_upgrade_decisions, priorities[i].__class__))

        # Wall (if not defensive)
        if self.stance != Stance.DEFENSIVE:
            decisions.append(self.choose(self.possible_upgrade_decisions, UpgradeWallDecision))

        if self.village.get_iron() == self.village.get_warehouse().capacity() or \
           self.village.get_stone() == self.village.get_warehouse().capacity() or \
           self.village.get_wood() == self.village.get_warehouse().capacity():
            # Warehouse (if full of at least one resource)
            decisions.append(self.choose(self.possible_upgrade_decisions, UpgradeWarehouseDecision))
            # Farm (if warehouse is full of at least one resource, just to dump resources)
            decisions.append(self.choose(self.possible_upgrade_decisions, UpgradeFarmDecision))

        # Nothing
        decisions.append(self.choose(self.possible_upgrade_decisions, UpgradeNothingDecision))

        return self.final_decision(decisions)

    # RECRUIT DECISION

    def recruit_decision(self):
        self.possible_recruit_decisions = self.recruit_options()
        action = self.recruit_filter()
        assert issubclass(action.__class__, RecruitDecision)
        return action.execute(ceil(action.n * self.troop_focus * random.uniform(0.5, 1.0)))

    def recruit_options(self):
        options = []

        # Won't recruit more spies if it has more than 5, and can only recruit 3 spies at once
        how_many_spies = self.how_many_can_recruit(self.village.get_spies())
        if how_many_spies > 0 and self.village.get_spies().get_n() <= 5:
            options.append(RecruitSpiesDecision(self, min(how_many_spies, 3)))

        how_many_warriors = self.how_many_can_recruit(self.village.get_warriors())
        if how_many_warriors > 0:
            options.append(RecruitWarriorsDecision(self, how_many_warriors))

        how_many_archers = self.how_many_can_recruit(self.village.get_archers())
        if how_many_archers > 0:
            options.append(RecruitArchersDecision(self, how_many_archers))

        how_many_catapults = self.how_many_can_recruit(self.village.get_catapults())
        if how_many_catapults > 0:
            options.append(RecruitCatapultsDecision(self, how_many_catapults))

        how_many_cavalrymen = self.how_many_can_recruit(self.village.get_cavalrymen())
        if how_many_cavalrymen > 0:
            options.append(RecruitCavalrymenDecision(self, how_many_cavalrymen))

        if self.village.get_spies().get_n() > 0:
            options.append(DemoteSpiesDecision(self, self.village.get_spies().get_n()))

        if self.village.get_warriors().get_n() > 0:
            options.append(DemoteWarriorsDecision(self, self.village.get_warriors().get_n()))

        if self.village.get_archers().get_n() > 0:
            options.append(DemoteArchersDecision(self, self.village.get_archers().get_n()))

        if self.village.get_catapults().get_n() > 0:
            options.append(DemoteCatapultsDecision(self, self.village.get_catapults().get_n()))

        if self.village.get_cavalrymen().get_n() > 0:
            options.append(DemoteCavalrymenDecision(self, self.village.get_cavalrymen().get_n()))

        options.append(RecruitNothingDecision(self))

        return options

    def recruit_filter(self):
        # Priority system:
        # - If farm is maxed out, full and has at least 20 non-cavalrymen, demote 20 units (to replace with cavalrymen)
        # - Spies
        # - Cavalrymen
        # - Catapults (if offensive)
        # - Archers (if defensive)
        # - Warriors
        # - Nothing

        decisions = []

        # Demote troops to replace with cavalrymen (prioritize demoting warriors)
        if self.village.get_farm().is_max_level() and self.village.get_farm().capacity() == self.village.get_troops():
            decisions.append(self.choose(self.possible_recruit_decisions, DemoteWarriorsDecision, demote_max=20))
            if self.stance == Stance.OFFENSIVE:
                decisions.append(self.choose(self.possible_recruit_decisions, DemoteArchersDecision, demote_max=20))
            if self.stance == Stance.DEFENSIVE:
                decisions.append(self.choose(self.possible_recruit_decisions, DemoteCatapultsDecision, demote_max=20))
            decisions.append(self.choose(self.possible_recruit_decisions, DemoteArchersDecision, demote_max=20))
            decisions.append(self.choose(self.possible_recruit_decisions, DemoteCatapultsDecision, demote_max=20))

        # Recruit spies, cavalrymen, {catapults / archers / -}, warriors, nothing
        decisions.append(self.choose(self.possible_recruit_decisions, RecruitSpiesDecision))
        decisions.append(self.choose(self.possible_recruit_decisions, RecruitCavalrymenDecision))
        if self.stance == Stance.OFFENSIVE:
            decisions.append(self.choose(self.possible_recruit_decisions, RecruitCatapultsDecision))
        elif self.stance == Stance.DEFENSIVE:
            decisions.append(self.choose(self.possible_recruit_decisions, RecruitArchersDecision))
        decisions.append(self.choose(self.possible_recruit_decisions, RecruitWarriorsDecision))
        decisions.append(self.choose(self.possible_recruit_decisions, RecruitNothingDecision))

        return self.final_decision(decisions)

    # SPYING DECISION

    def spying_decision(self):
        self.possible_spying_decisions = self.spying_options()
        action = self.spying_filter()
        assert issubclass(action.__class__, SpyingDecision)
        return action.execute()

    def spying_options(self):
        if self.village.get_spies().get_n() == 0:
            return [SpyNothingDecision(self)]
        options = []
        for village in self.get_other_villages():
            options.append(SpyVillageDecision(self, village))
        options.append(SpyNothingDecision(self))
        return options

    def spying_filter(self):
        # Priority system:
        # - If village has no spies, don't spy (obviously)
        # - Among villages that haven't been spied in the last 10 turns, pick one at random

        decisions = []

        # Only possible decision is SpyNothing - do that
        if len(self.possible_spying_decisions) == 1:
            return self.possible_spying_decisions[0]

        # Initialize list with all possible villages that can be spied, then remove villages with recent espionages
        villages_to_spy = [decision.enemy_village_name
                           for decision in self.possible_spying_decisions
                           if isinstance(decision, SpyVillageDecision)]
        for espionage in self.spy_log:
            if espionage.get_turn() > self.turn - 10 and espionage.enemy_village_name in villages_to_spy:
                villages_to_spy.remove(espionage.enemy_village_name)

        # Out of the villages that can be spied, spy one at random
        if len(villages_to_spy) > 0:
            village_to_spy = random.choice(villages_to_spy)
            for decision in self.possible_spying_decisions:
                if decision.enemy_village_name == village_to_spy:
                    decisions.append(decision)

        decisions.append(self.choose(self.possible_spying_decisions, SpyNothingDecision))

        return self.final_decision(decisions)

    # ATTACK DECISION

    def attack_decision(self):
        self.possible_attack_decisions = self.attack_options()
        action = self.attack_filter()
        assert issubclass(action.__class__, AttackDecision)
        return action.execute(action.n_warriors, action.n_archers, action.n_catapults, action.n_cavalrymen)

    def attack_options(self):
        if self.village.get_troops() - self.village.get_spies().get_n() == 0:
            return [AttackNothingDecision(self)]
        options = []
        for village in self.get_other_villages():
            options.append(AttackVillageDecision(self,
                                                 self.village.get_warriors().get_n(),
                                                 self.village.get_archers().get_n(),
                                                 self.village.get_catapults().get_n(),
                                                 self.village.get_cavalrymen().get_n(),
                                                 village))
        options.append(AttackNothingDecision(self))
        return options

    def attack_filter(self):
        # Priority system:
        # - If agent has victorious attacks in the {stance.get_last_turns()} against villages and
        #   is not in recovery mode, attack one of those villages at random
        # - If agent has an espionage in the {stance.get_last_turns()} and
        #   its own attack_power is greater than {stance.get_magnitude()} times the defense power of the spied village,
        #   attack the one with the largest difference (easiest win)

        decisions = []

        # If defeated recently, enter recovery mode
        recovery = False
        for report in self.report_log:
            if report.get_loser() == self.village.get_name() and \
               report.get_turn() > self.turn - self.stance.get_recovery_turns():
                recovery = True

        # Attack village recently victorious against
        villages_to_attack = []
        for report in self.report_log:
            if not recovery and \
               report.get_turn() > self.turn - self.stance.get_last_turns() and \
               report.get_winner() == self.village.get_name() and \
               report.get_attacking_village() == self.village.get_name() and \
               report.get_defending_village() in self.other_villages:
                villages_to_attack.append(report.get_defending_village())

        if len(villages_to_attack) > 0:
            village_to_attack = random.choice(villages_to_attack)
            for decision in self.possible_attack_decisions:
                if decision.enemy_village_name == village_to_attack:
                    decision.n_warriors = ceil(self.stance.get_warrior_send_ratio() * decision.n_warriors)
                    decision.n_archers = ceil(self.stance.get_archer_send_ratio() * decision.n_archers)
                    decision.n_catapults = ceil(self.stance.get_catapult_send_ratio() * decision.n_catapults)
                    decision.n_cavalrymen = ceil(self.stance.get_cavalrymen_send_ratio() * decision.n_cavalrymen)
                    # Only send an attack if agent has troops suitable for attacking
                    if decision.n_warriors + decision.n_archers + decision.n_catapults + decision.n_cavalrymen > 0:
                        decisions.append(decision)

        # Attack village that recent espionage claims to be favored against
        # Possibilities list is a list of tuples (enemy village name, power difference)
        possibilities = []
        for espionage in self.spy_log:
            if espionage.get_turn() > self.turn - self.stance.get_last_turns() and \
               self.village.get_attack_power() > \
               self.stance.get_magnitude() * espionage.get_spied_village().get_defense_power() and \
               espionage.get_enemy_village_name() in self.other_villages:
                possibilities.append((espionage.get_enemy_village_name(),
                                      self.stance.get_attack_power(self) -
                                      espionage.get_spied_village().get_defense_power()))

        if len(possibilities) > 0:
            village_to_attack = possibilities[0]
            for village in possibilities[1:]:
                if village[1] > village_to_attack[1]:
                    village_to_attack = village
            for decision in self.possible_attack_decisions:
                if decision.enemy_village_name == village_to_attack[0]:
                    decision.n_warriors = ceil(self.stance.get_warrior_send_ratio() * decision.n_warriors)
                    decision.n_archers = ceil(self.stance.get_archer_send_ratio() * decision.n_archers)
                    decision.n_catapults = ceil(self.stance.get_catapult_send_ratio() * decision.n_catapults)
                    decision.n_cavalrymen = ceil(self.stance.get_cavalrymen_send_ratio() * decision.n_cavalrymen)
                    # Only send an attack if agent has troops suitable for attacking
                    if decision.n_warriors + decision.n_archers + decision.n_catapults + decision.n_cavalrymen > 0:
                        decisions.append(decision)

        decisions.append(self.choose(self.possible_attack_decisions, AttackNothingDecision))

        return self.final_decision(decisions)

    # AUX

    # Update state-related variables of the reactive agent
    def update_state(self):
        super().update_state()
        for report in self.get_report_log():
            if report.get_turn() == self.turn - 1:
                if report.get_attacking_village() == self.village.get_name():
                    self.turns_since_last_attack = 0
                    if report.get_loser() == self.village.get_name():
                        self.turns_since_last_attack_loss = 0
                else:
                    self.turns_since_last_defense = 0
                    if report.get_loser() == self.village.get_name():
                        self.turns_since_last_defense_loss = 0

        self.turns_since_last_attack += 1
        self.turns_since_last_defense += 1
        self.turns_since_last_attack_loss += 1
        self.turns_since_last_defense_loss += 1
        self.previous_attack_powers.append(self.village.get_attack_power())
        self.previous_attack_powers.pop(0)

    # Adapt agent stance given the game-specific circumstances
    def change_stance(self):
        # Stance changes abide to the following rules:
        # - If health is below 25%, immediately adopt defensive stance
        # - If agent is currently defensive:
        # --- If agent has not been involved in any fights in a certain number of turns, become neutral
        # - If agent is currently neutral:
        # --- If agent has recently lost at least 95% of its attack power, become defensive
        # --- If agent has not been involved in any fights in a certain number of turns, become offensive
        # If agent is currently offensive:
        # --- If agent has recently lost at least 95% of its attack power, become defensive
        # --- If agent has recently lost at least two thirds of its attack power, become neutral

        if self.stance != Stance.DEFENSIVE and self.village.get_health() < (1/4) * self.village.MAX_HEALTH:
            new_stance = Stance.DEFENSIVE
            self.stance_history.append((new_stance, self.turn))
            self.stance = new_stance
            return

        if self.stance == Stance.DEFENSIVE:
            if self.turns_since_last_attack > self.stance.get_turns_without_fighting() and \
               self.turns_since_last_defense > self.stance.get_turns_without_fighting() and \
               self.turn > 75:
                new_stance = Stance.NEUTRAL
                self.stance_history.append((new_stance, self.turn))
                self.stance = new_stance
        elif self.stance == Stance.NEUTRAL:
            if self.village.get_attack_power() < 0.05 * max(self.previous_attack_powers):
                new_stance = Stance.DEFENSIVE
                self.stance_history.append((new_stance, self.turn))
                self.stance = new_stance
            elif self.turns_since_last_attack > self.stance.get_turns_without_fighting() and \
                    self.turns_since_last_defense > self.stance.get_turns_without_fighting() and \
                    self.turn > 100:
                new_stance = Stance.OFFENSIVE
                self.stance_history.append((new_stance, self.turn))
                self.stance = new_stance
        else:
            if self.village.get_attack_power() < 0.05 * max(self.previous_attack_powers):
                new_stance = Stance.DEFENSIVE
                self.stance_history.append((new_stance, self.turn))
                self.stance = new_stance
            elif self.village.get_attack_power() < (1/3) * max(self.previous_attack_powers):
                new_stance = Stance.NEUTRAL
                self.stance_history.append((new_stance, self.turn))
                self.stance = new_stance

    # Return a specific decision given a list of decisions and a decision type
    def choose(self, options, decision_type, demote_max=None):
        for decision in options:
            if isinstance(decision, decision_type):
                if demote_max is not None:
                    return decision_type(self, min(20, decision.n))
                else:
                    return decision
        return None

    # Return the highest priority decision (the one that comes first)
    @staticmethod
    def final_decision(decisions):
        for decision in decisions:
            if decision is not None:
                return decision
        raise Exception("Should not get here! Failed in a filter()")

    # Compute how many units of a specific unit type can be recruited given the resources and farm space in the village
    def how_many_can_recruit(self, troop):
        if self.village.get_barracks().get_level() < troop.MIN_BARRACKS_LEVEL:
            return 0
        n = 0
        done = False

        while not done:
            n += 1
            village_resources = [self.village.get_iron(), self.village.get_stone(), self.village.get_wood()]
            troop_costs = troop.cost(n)
            for c1, c2 in zip(village_resources, troop_costs):
                if c1 < c2:
                    n -= 1
                    done = True
                    break

        return min(n, self.village.get_farm().capacity() - self.village.get_troops())

    def get_starting_stance(self):
        return self.stance_history[0][0]

    def get_ending_stance(self):
        return self.stance_history[-1][0]
