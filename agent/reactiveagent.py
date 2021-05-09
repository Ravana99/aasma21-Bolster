from random import random
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
        # Priority system as follows (SUBJECT TO CHANGES):
        # - Upgrade farm if farm is full
        # - Upgrade warehouse if production of a resource is > 0.5 * warehouse capacity
        # - Upgrade resource camp, prioritizing resource with lowest amount
        # - Upgrade barracks
        # - Upgrade wall
        # - Upgrade warehouse if full
        # - Upgrade farm if warehouse is full (just as a resource dump)
        # - Upgrade nothing

        # Farm
        if self.village.get_troops() == self.get_farm().capacity():
            for decision in self.possible_upgrade_decisions:
                if isinstance(decision, UpgradeFarmDecision):
                    return decision

        # Warehouse (if producing a lot)
        if self.village.get_mine().production() > 0.5 * self.village.get_warehouse().capacity() or \
           self.village.get_quarry().production() > 0.5 * self.village.get_warehouse().capacity() or \
           self.village.get_sawmill().production() > 0.5 * self.village.get_warehouse().capacity():
            for decision in self.possible_upgrade_decisions:
                if isinstance(decision, UpgradeWarehouseDecision):
                    return decision

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
            for decision in self.possible_upgrade_decisions:
                if isinstance(decision, priorities[i].__class__):
                    return decision

        # Barracks
        for decision in self.possible_upgrade_decisions:
            if isinstance(decision, UpgradeBarracksDecision):
                return decision

        # Wall
        for decision in self.possible_upgrade_decisions:
            if isinstance(decision, UpgradeWallDecision):
                return decision

        if self.village.get_iron() == self.village.get_warehouse().capacity() or \
           self.village.get_stone() == self.village.get_warehouse().capacity() or \
           self.village.get_wood() == self.village.get_warehouse().capacity():
            # Warehouse (if full of at least one resource)
            for decision in self.possible_upgrade_decisions:
                if isinstance(decision, UpgradeWarehouseDecision):
                    return decision
            # Farm (if warehouse is full of at least one resource, just to dump resources)
            for decision in self.possible_upgrade_decisions:
                if isinstance(decision, UpgradeFarmDecision):
                    return decision

        # Nothing
        for decision in self.possible_upgrade_decisions:
            if isinstance(decision, UpgradeNothingDecision):
                return decision

        raise Exception("Should not get here! Failed in upgrade_filter()")

    def recruit_decision(self):
        # TODO: add way for agent to adapt its stance based on new reports and new espionages
        self.possible_recruit_decisions = self.recruit_options()
        action = self.recruit_filter()
        assert issubclass(action.__class__, RecruitDecision)
        return action.execute(ceil(action.n * self.troop_focus * random()))

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
        # - If farm is maxed, full and has at least 20 warriors, demote 20 warriors (to replace with better troops)
        # - If neutral:
        # --- Spies
        # --- Cavalrymen
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
        if self.village.get_farm().is_max_level() and self.village.get_farm().capacity() == self.village.get_troops():
            for decision in self.possible_recruit_decisions:
                if isinstance(decision, DemoteWarriorsDecision) and decision.n >= 20:
                    return DemoteWarriorsDecision(self, 20)

        if self.stance == Stance.NEUTRAL:
            for decision in self.possible_recruit_decisions:
                if isinstance(decision, RecruitSpiesDecision):
                    return decision
            for decision in self.possible_recruit_decisions:
                if isinstance(decision, RecruitCavalrymenDecision):
                    return decision
            for decision in self.possible_recruit_decisions:
                if isinstance(decision, RecruitWarriorsDecision):
                    return decision
            for decision in self.possible_recruit_decisions:
                if isinstance(decision, RecruitNothingDecision):
                    return decision

        elif self.stance == Stance.OFFENSIVE:
            for decision in self.possible_recruit_decisions:
                if isinstance(decision, RecruitCavalrymenDecision):
                    return decision
            for decision in self.possible_recruit_decisions:
                if isinstance(decision, RecruitCatapultsDecision):
                    return decision
            for decision in self.possible_recruit_decisions:
                if isinstance(decision, RecruitSpiesDecision):
                    return decision
            for decision in self.possible_recruit_decisions:
                if isinstance(decision, RecruitWarriorsDecision):
                    return decision
            for decision in self.possible_recruit_decisions:
                if isinstance(decision, RecruitNothingDecision):
                    return decision

        else:
            for decision in self.possible_recruit_decisions:
                if isinstance(decision, RecruitCavalrymenDecision):
                    return decision
            for decision in self.possible_recruit_decisions:
                if isinstance(decision, RecruitArchersDecision):
                    return decision
            for decision in self.possible_recruit_decisions:
                if isinstance(decision, RecruitSpiesDecision):
                    return decision
            for decision in self.possible_recruit_decisions:
                if isinstance(decision, RecruitWarriorsDecision):
                    return decision
            for decision in self.possible_recruit_decisions:
                if isinstance(decision, RecruitNothingDecision):
                    return decision

        raise Exception("Should not get here! Failed in recruit_filter()")

    def spying_decision(self):
        self.possible_spying_decisions = self.spying_options()
        action = self.spying_filter()
        assert issubclass(action.__class__, SpyingDecision)
        return action.execute()

    def spying_options(self):
        return [SpyNothingDecision(self)]

    def spying_filter(self):
        return self.possible_spying_decisions[0]

    def attack_decision(self):
        self.possible_attack_decisions = self.attack_options()
        action = self.attack_filter()
        assert issubclass(action.__class__, AttackDecision)
        return action.execute()

    def attack_options(self):
        return [AttackNothingDecision(self)]

    def attack_filter(self):
        return self.possible_attack_decisions[0]

    # AUX

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
