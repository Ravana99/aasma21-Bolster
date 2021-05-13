import random
from agent.agent import Agent
from agent.decisions import *
from math import ceil
import enum


class Stance(enum.Enum):
    NEUTRAL = 0
    OFFENSIVE = 1
    DEFENSIVE = 2


class ReactiveAgent(Agent):

    def __init__(self, i, stance):
        super().__init__(i)
        self.stance = stance

    possible_upgrade_decisions = []
    possible_recruit_decisions = []
    possible_spying_decisions = []
    possible_attack_decisions = []
    stance = Stance.DEFENSIVE
    troop_focus = 0.5

    def upgrade_decision(self):
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
        # - Upgrade resource camp, prioritizing resource with lowest amount
        # - Upgrade barracks
        # - Upgrade wall
        # - Upgrade warehouse if full
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

        # Wall
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

    def recruit_decision(self):
        # TODO: add way for agent to adapt its stance based on recent reports and recent espionages
        self.possible_recruit_decisions = self.recruit_options()
        action = self.recruit_filter()
        assert issubclass(action.__class__, RecruitDecision)
        return action.execute(ceil(action.n * self.troop_focus * random.random()))

    def recruit_options(self):
        options = []

        # Won't recruit more spies if it has 5 already, and can only recruit 3 spies at once
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
        # - If farm is maxed, full and has at least 20 non-cavalrymen, demote 20 units (to replace with cavalrymen)
        # - If neutral:
        # --- Cavalrymen
        # --- Spies
        # --- Warriors
        # --- Nothing
        # - If offensive:
        # --- Cavalrymen
        # --- Catapults
        # --- Spies
        # --- Warriors
        # --- Nothing
        # - If defensive:
        # --- Cavalrymen
        # --- Archers
        # --- Spies
        # --- Warriors
        # --- Nothing

        decisions = []

        if self.village.get_farm().is_max_level() and self.village.get_farm().capacity() == self.village.get_troops():
            decisions.append(self.choose(self.possible_recruit_decisions, DemoteWarriorsDecision, demote_max=20))
            if self.stance == Stance.OFFENSIVE:
                decisions.append(self.choose(self.possible_recruit_decisions, DemoteArchersDecision, demote_max=20))
            if self.stance == Stance.DEFENSIVE:
                decisions.append(self.choose(self.possible_recruit_decisions, DemoteCatapultsDecision, demote_max=20))
            decisions.append(self.choose(self.possible_recruit_decisions, DemoteArchersDecision, demote_max=20))
            decisions.append(self.choose(self.possible_recruit_decisions, DemoteCatapultsDecision, demote_max=20))

        if self.stance == Stance.NEUTRAL:
            decisions.append(self.choose(self.possible_recruit_decisions, RecruitSpiesDecision))
            decisions.append(self.choose(self.possible_recruit_decisions, RecruitCavalrymenDecision))
            decisions.append(self.choose(self.possible_recruit_decisions, RecruitWarriorsDecision))
            decisions.append(self.choose(self.possible_recruit_decisions, RecruitNothingDecision))

        elif self.stance == Stance.OFFENSIVE:
            decisions.append(self.choose(self.possible_recruit_decisions, RecruitSpiesDecision))
            decisions.append(self.choose(self.possible_recruit_decisions, RecruitCavalrymenDecision))
            decisions.append(self.choose(self.possible_recruit_decisions, RecruitCatapultsDecision))
            decisions.append(self.choose(self.possible_recruit_decisions, RecruitWarriorsDecision))
            decisions.append(self.choose(self.possible_recruit_decisions, RecruitNothingDecision))

        else:
            decisions.append(self.choose(self.possible_recruit_decisions, RecruitSpiesDecision))
            decisions.append(self.choose(self.possible_recruit_decisions, RecruitCavalrymenDecision))
            decisions.append(self.choose(self.possible_recruit_decisions, RecruitArchersDecision))
            decisions.append(self.choose(self.possible_recruit_decisions, RecruitWarriorsDecision))
            decisions.append(self.choose(self.possible_recruit_decisions, RecruitNothingDecision))

        return self.final_decision(decisions)

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

        if len(self.possible_spying_decisions) == 1:
            return self.possible_spying_decisions[0]

        villages_to_spy = [decision.enemy_village_name
                           for decision in self.possible_spying_decisions
                           if isinstance(decision, SpyVillageDecision)]

        for espionage in self.spy_log:
            if espionage.get_turn() > self.turn - 10 and espionage.enemy_village_name in villages_to_spy:
                villages_to_spy.remove(espionage.enemy_village_name)

        if len(villages_to_spy) > 0:
            village_to_spy = random.choice(villages_to_spy)
            for decision in self.possible_spying_decisions:
                if decision.enemy_village_name == village_to_spy:
                    decisions.append(decision)

        decisions.append(self.choose(self.possible_spying_decisions, SpyNothingDecision))

        return self.final_decision(decisions)

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
        # - If defeated in the last {recovery_turns}, don't attack
        # - If agent has a victorious attack in the {last_turns} against villages, attack 1 of those at random
        # - If agent has an espionage in the {last_turns} and self.attack_power > {magnitude} * other.defense_power,
        #   attack the one with the largest difference (easiest win)

        if self.stance == Stance.NEUTRAL:
            recovery_turns = 5
            last_turns = 5
            magnitude = 1.1
            attack_power = self.village.get_attack_power_no_archers()
            warrior_send_ratio = 1
            archer_send_ratio = 0
            catapult_send_ratio = 1
            cavalrymen_send_ratio = 1
        elif self.stance == Stance.OFFENSIVE:
            recovery_turns = 3
            last_turns = 10
            magnitude = 1
            attack_power = self.village.get_attack_power()
            warrior_send_ratio = 1
            archer_send_ratio = 1
            catapult_send_ratio = 1
            cavalrymen_send_ratio = 1
        else:
            recovery_turns = 10
            last_turns = 3
            magnitude = 2.5
            attack_power = self.village.get_attack_power_no_archers()
            warrior_send_ratio = 0.5
            archer_send_ratio = 0
            catapult_send_ratio = 1
            cavalrymen_send_ratio = 0.5

        decisions = []

        recovery = False
        for report in self.report_log:
            if report.get_loser() == self.village.get_name() and report.get_turn() > self.turn - recovery_turns:
                recovery = True

        villages_to_attack = []

        for report in self.report_log:
            if not recovery and \
               report.get_turn() > self.turn - last_turns and \
               report.get_winner() == self.village.get_name() and \
               report.get_attacking_village() == self.village.get_name() and \
               report.get_defending_village() in self.other_villages:
                villages_to_attack.append(report.get_defending_village())

        if len(villages_to_attack) > 0:
            village_to_attack = random.choice(villages_to_attack)
            for decision in self.possible_attack_decisions:
                if decision.enemy_village_name == village_to_attack:
                    decision.n_warriors = ceil(warrior_send_ratio * decision.n_warriors)
                    decision.n_archers = ceil(archer_send_ratio * decision.n_archers)
                    decision.n_catapults = ceil(catapult_send_ratio * decision.n_catapults)
                    decision.n_cavalrymen = ceil(cavalrymen_send_ratio * decision.n_cavalrymen)
                    # If agent has no troops suitable for attacking, don't send one
                    if decision.n_warriors + decision.n_archers + decision.n_catapults + decision.n_cavalrymen > 0:
                        decisions.append(decision)

        possibilities = []

        for espionage in self.spy_log:
            if espionage.get_turn() > self.turn - last_turns and \
               self.village.get_attack_power() > magnitude * espionage.get_spied_village().get_defense_power() and \
               espionage.get_enemy_village_name() in self.other_villages:
                possibilities.append((espionage.get_enemy_village_name(),
                                      attack_power - espionage.get_spied_village().get_defense_power()))

        if len(possibilities) > 0:
            village_to_attack = possibilities[0]
            for village in possibilities[1:]:
                if village[1] > village_to_attack[1]:
                    village_to_attack = village
            for decision in self.possible_attack_decisions:
                if decision.enemy_village_name == village_to_attack[0]:
                    decision.n_warriors = ceil(warrior_send_ratio * decision.n_warriors)
                    decision.n_archers = ceil(archer_send_ratio * decision.n_archers)
                    decision.n_catapults = ceil(catapult_send_ratio * decision.n_catapults)
                    decision.n_cavalrymen = ceil(cavalrymen_send_ratio * decision.n_cavalrymen)
                    # If agent has no troops suitable for attacking, don't send one
                    if decision.n_warriors + decision.n_archers + decision.n_catapults + decision.n_cavalrymen > 0:
                        decisions.append(decision)

        decisions.append(self.choose(self.possible_attack_decisions, AttackNothingDecision))

        return self.final_decision(decisions)

    # AUX

    def choose(self, options, decision_type, demote_max=None):
        for decision in options:
            if isinstance(decision, decision_type):
                if demote_max is not None:
                    return decision_type(self, min(20, decision.n))
                else:
                    return decision
        return None

    @staticmethod
    def final_decision(decisions):
        for decision in decisions:
            if decision is not None:
                return decision
        raise Exception("Should not get here! Failed in a filter()")

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
