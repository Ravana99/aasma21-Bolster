from village import Village
from agent.decisions import *
from buildings.barracks import Barracks
from buildings.farm import Farm
from buildings.mine import Mine
from buildings.quarry import Quarry
from buildings.sawmill import Sawmill
from buildings.wall import Wall
from buildings.warehouse import Warehouse


class Agent:
    """DO NOT INSTANTIATE!"""

    def __init__(self, i):
        self.village = Village(i)
        self.name = "Agent " + str(i)
        self.other_villages = []
        self.report_log = []
        self.spy_log = []
        self.turn = 0
        self.decision_log = []
        self.attack_power_history = [(0, 0)]
        self.defense_power_history = [(0, 0)]
        self.hp_history = [(self.village.MAX_HEALTH, 0)]
        self.troop_casualties_history = []
        self.prosperity_rating_history = [(self.village.get_prosperity_rating(), 0)]
        self.successful_attacks = 0
        self.failed_attacks = 0
        self.successful_defenses = 0
        self.failed_defenses = 0
        self.warrior_casualties = 0
        self.archer_casualties = 0
        self.catapult_casualties = 0
        self.cavalrymen_casualties = 0

    def upgrade_decision(self):
        raise NotImplementedError()

    def recruit_decision(self):
        raise NotImplementedError()

    def spying_decision(self):
        raise NotImplementedError()

    def attack_decision(self):
        raise NotImplementedError()

    # SENSORS - BUILDINGS

    def get_barracks(self):
        return self.village.get_barracks()

    def get_wall(self):
        return self.village.get_wall()

    def get_mine(self):
        return self.village.get_mine()

    def get_quarry(self):
        return self.village.get_quarry()

    def get_sawmill(self):
        return self.village.get_sawmill()

    def get_farm(self):
        return self.village.get_farm()

    def get_warehouse(self):
        return self.village.get_warehouse()

    # SENSORS - TROOPS

    def get_warriors(self):
        return self.village.get_warriors()

    def get_archers(self):
        return self.village.get_archers()

    def get_catapults(self):
        return self.village.get_catapults()

    def get_cavalrymen(self):
        return self.village.get_cavalrymen()

    def get_troops(self):
        return self.village.get_troops()

    # SENSORS - STATS

    def get_health(self):
        return self.village.get_health()

    def get_iron(self):
        return self.village.get_iron()

    def get_stone(self):
        return self.village.get_stone()

    def get_wood(self):
        return self.village.get_wood()

    # ACTUATORS - UPGRADES

    def upgrade_barracks(self):
        self.village.upgrade_barracks()

    def upgrade_farm(self):
        self.village.upgrade_farm()

    def upgrade_mine(self):
        self.village.upgrade_mine()

    def upgrade_quarry(self):
        self.village.upgrade_quarry()

    def upgrade_sawmill(self):
        self.village.upgrade_sawmill()

    def upgrade_wall(self):
        self.village.upgrade_wall()

    def upgrade_warehouse(self):
        self.village.upgrade_warehouse()

    @staticmethod
    def upgrade_nothing():
        pass

    # ACTUATORS - RECRUITMENTS

    def recruit_spies(self, n):
        self.village.recruit_spies(n)

    def recruit_warriors(self, n):
        self.village.recruit_warriors(n)

    def recruit_archers(self, n):
        self.village.recruit_archers(n)

    def recruit_catapults(self, n):
        self.village.recruit_catapults(n)

    def recruit_cavalrymen(self, n):
        self.village.recruit_cavalrymen(n)

    def demote_spies(self, n):
        self.village.demote_spies(n)

    def demote_warriors(self, n):
        self.village.demote_warriors(n)

    def demote_archers(self, n):
        self.village.demote_archers(n)

    def demote_catapults(self, n):
        self.village.demote_catapults(n)

    def demote_cavalrymen(self, n):
        self.village.demote_cavalrymen(n)

    @staticmethod
    def recruit_nothing():
        pass

    # ACTUATORS - SPYING

    def spy(self, enemy_village_name):
        return self.village.spy(enemy_village_name)

    @staticmethod
    def spy_nothing():
        return

    # ACTUATORS - ATTACKS

    def send_attack(self, n_warriors, n_archers, n_catapults, n_cavalrymen, enemy_village_name):
        return self.village.create_attacking_army(n_warriors, n_archers, n_catapults, n_cavalrymen, enemy_village_name)

    @staticmethod
    def attack_nothing():
        return

    # AUX

    def get_name(self):
        return self.name

    def get_report_log(self):
        return self.report_log

    def get_spy_log(self):
        return self.spy_log

    def add_report(self, report):
        self.report_log.insert(0, report)

    def add_espionage(self, espionage):
        self.spy_log.insert(0, espionage)

    def add_decision(self, decision):
        self.decision_log.insert(0, decision)

    def remove_other_village(self, name):
        self.other_villages.remove(name)

    def get_village(self):
        return self.village

    def get_other_villages(self):
        return self.other_villages

    def set_other_villages(self, villages):
        self.other_villages = villages

    def set_turn(self, turn):
        self.turn = turn

    def can_upgrade(self, building):
        if building.is_max_level():
            return False
        village_resources = [self.village.get_iron(), self.village.get_stone(), self.village.get_wood()]
        building_costs = building.get_cost_of_upgrade()
        for c1, c2 in zip(village_resources, building_costs):
            if c1 < c2:
                return False
        return True

    def building_to_upgrade_action(self, building):
        if isinstance(building, Barracks):
            return UpgradeBarracksDecision(self)
        elif isinstance(building, Farm):
            return UpgradeFarmDecision(self)
        elif isinstance(building, Mine):
            return UpgradeMineDecision(self)
        elif isinstance(building, Quarry):
            return UpgradeQuarryDecision(self)
        elif isinstance(building, Sawmill):
            return UpgradeSawmillDecision(self)
        elif isinstance(building, Wall):
            return UpgradeWallDecision(self)
        elif isinstance(building, Warehouse):
            return UpgradeWarehouseDecision(self)
        else:
            return UpgradeNothingDecision(self)

    @staticmethod
    def cost_of_upgrade_action(action):
        if isinstance(action, UpgradeNothingDecision):
            return [0, 0, 0]
        else:
            return action.to_building().get_cost_of_upgrade()

    # Update state-related variables
    def update_state(self):
        for report in self.get_report_log():
            if report.get_turn() == self.turn - 1:
                # Village attacked last turn
                if report.get_attacking_village() == self.village.get_name():
                    if report.get_loser() == self.village.get_name():
                        self.failed_attacks += 1
                    else:
                        self.successful_attacks += 1
                    casualties = report.get_attacking_casualties()
                # Village defended last turn
                else:
                    if report.get_loser() == self.village.get_name():
                        self.failed_defenses += 1
                    else:
                        self.successful_defenses += 1
                    casualties = report.get_defending_casualties()
                # Update overall casualty information
                if sum(casualties.values()) > 0:
                    self.troop_casualties_history.append((casualties, self.turn))
                    self.warrior_casualties += casualties["warriors"]
                    self.archer_casualties += casualties["archers"]
                    self.catapult_casualties += casualties["catapults"]
                    self.cavalrymen_casualties += casualties["cavalrymen"]

        if self.village.health != self.hp_history[-1][0]:
            self.hp_history.append((self.village.health, self.turn))
        if self.village.get_attack_power() != self.attack_power_history[-1][0]:
            self.attack_power_history.append((self.village.get_attack_power(), self.turn))
        if self.village.get_defense_power() != self.defense_power_history[-1][0]:
            self.defense_power_history.append((self.village.get_defense_power(), self.turn))
        if self.village.get_prosperity_rating() != self.prosperity_rating_history[-1][0]:
            self.prosperity_rating_history.append((self.village.get_prosperity_rating(), self.turn))
