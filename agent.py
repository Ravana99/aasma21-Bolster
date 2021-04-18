from village import Village


class Agent:

    def __init__(self, i):
        self.village = Village(i)
        self.name = "Agent " + str(i)
        self.other_villages = []
        self.report_log = []

    def upgrade_decision(self):
        raise NotImplementedError()

    def recruit_decision(self):
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

    def recruit_warriors(self, n):
        self.village.recruit_warriors(n)

    def recruit_archers(self, n):
        self.village.recruit_archers(n)

    def recruit_catapults(self, n):
        self.village.recruit_catapults(n)

    def recruit_cavalrymen(self, n):
        self.village.recruit_cavalrymen(n)

    @staticmethod
    def recruit_nothing():
        pass

    def demote_warriors(self, n):
        self.village.demote_warriors(n)

    def demote_archers(self, n):
        self.village.demote_archers(n)

    def demote_catapults(self, n):
        self.village.demote_catapults(n)

    def demote_cavalrymen(self, n):
        self.village.demote_cavalrymen(n)

    @staticmethod
    def demote_nothing():
        pass

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

    def add_report(self, report):
        self.report_log.insert(0, report)

    def remove_other_village(self, name):
        self.other_villages.remove(name)

    def get_village(self):
        return self.village

    def set_other_villages(self, villages):
        self.other_villages = villages
