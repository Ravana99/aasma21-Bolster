from village import Village


class Agent:

    def __init__(self, i):
        self.village = Village(i)
        self.name = "Agent " + str(i)
        self.other_villages = []

    def decision(self):
        raise NotImplementedError()

    # SENSORS - BUILDINGS

    def get_barracks(self):
        return self.village.get_barracks()

    def get_wall(self):
        return self.village.get_wall()

    def get_mine(self):
        return self.village.get_mine()

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

    def get_troops(self):
        return self.village.get_troops()

    # SENSORS - STATS

    def get_health(self):
        return self.village.get_health()

    def get_stone(self):
        return self.village.get_stone()

    def was_attacked(self):
        return self.village.was_attacked()

    # ACTUATORS - UPGRADE

    def upgrade_barracks(self):
        self.village.upgrade_barracks()

    def upgrade_farm(self):
        self.village.upgrade_farm()

    def upgrade_mine(self):
        self.village.upgrade_mine()

    def upgrade_wall(self):
        self.village.upgrade_wall()

    def upgrade_warehouse(self):
        self.village.upgrade_warehouse()

    # ACTUATORS - RECRUITMENTS

    def recruit_warriors(self, n):
        self.village.recruit_warriors(n)

    def recruit_archers(self, n):
        self.village.recruit_archers(n)

    def recruit_catapults(self, n):
        self.village.recruit_catapults(n)

    def demote_warriors(self, n):
        self.village.demote_warriors(n)

    def demote_archers(self, n):
        self.village.demote_archers(n)

    def demote_catapults(self, n):
        self.village.demote_catapults(n)

    # OTHER

    def get_village(self):
        return self.village

    def set_other_villages(self, villages):
        self.other_villages = villages
