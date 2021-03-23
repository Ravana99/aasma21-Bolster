from buildings.barracks import Barracks
from buildings.farm import Farm
from buildings.mine import Mine
from buildings.wall import Wall
from buildings.warehouse import Warehouse
from troops.warriors import Warriors
from troops.archers import Archers
from troops.catapults import Catapults
from troops.army import Army


class Village:

    MAX_HEALTH = 1000
    STARTING_STONE = 100

    def __init__(self, i):
        self.name = "Village " + str(i)
        self.barracks = Barracks()
        self.farm = Farm()
        self.mine = Mine()
        self.wall = Wall()
        self.warehouse = Warehouse()
        self.health = Village.MAX_HEALTH
        self.stone = Village.STARTING_STONE
        self.warriors = Warriors()
        self.archers = Archers()
        self.catapults = Catapults()

    # GETTERS

    def get_name(self):
        return self.name

    def get_barracks(self):
        return self.barracks

    def get_farm(self):
        return self.farm

    def get_mine(self):
        return self.mine

    def get_wall(self):
        return self.wall

    def get_warehouse(self):
        return self.warehouse

    def get_health(self):
        return self.health

    def get_stone(self):
        return self.stone

    def get_warriors(self):
        return self.warriors

    def get_archers(self):
        return self.archers

    def get_catapults(self):
        return self.catapults

    def get_troops(self):
        return self.warriors.get_n() + self.archers.get_n() + self.catapults.get_n()

    # UPGRADES

    def upgrade_barracks(self):
        self.stone = self.barracks.upgrade(self.stone)

    def upgrade_farm(self):
        self.stone = self.farm.upgrade(self.stone)

    def upgrade_mine(self):
        self.stone = self.mine.upgrade(self.stone)

    def upgrade_wall(self):
        self.stone = self.wall.upgrade(self.stone)

    def upgrade_warehouse(self):
        self.stone = self.warehouse.upgrade(self.stone)

    # RECRUITMENTS

    def recruit_warriors(self, n):
        free_capacity = self.farm.capacity() - self.get_troops()
        self.stone = self.warriors.recruit(self.stone, n, self.barracks.get_level(), free_capacity)

    def recruit_archers(self, n):
        free_capacity = self.farm.capacity() - self.get_troops()
        self.stone = self.archers.recruit(self.stone, n, self.barracks.get_level(), free_capacity)

    def recruit_catapults(self, n):
        free_capacity = self.farm.capacity() - self.get_troops()
        self.stone = self.catapults.recruit(self.stone, n, self.barracks.get_level(), free_capacity)

    def demote_warriors(self, n):
        self.warriors.demote(n)

    def demote_archers(self, n):
        self.archers.demote(n)

    def demote_catapults(self, n):
        self.catapults.demote(n)

    # ATTACKS

    def create_attacking_army(self, n_warriors, n_archers, n_catapults, enemy_village_name):
        self.warriors.send_off(n_warriors)
        self.archers.send_off(n_archers)
        self.catapults.send_off(n_archers)
        return Army(n_warriors, n_archers, n_catapults,
                    self.name, enemy_village_name=enemy_village_name, attacking=True)

    def create_defensive_army(self):
        return Army(self.warriors.get_n(), self.archers.get_n(), self.catapults.get_n(), self.name, attacking=False)

    # STONE

    def add_stone(self, stone):
        self.stone = min(self.stone + stone, self.warehouse.capacity())

    def produce_stone(self):
        self.stone = min(self.stone + self.mine.production(), self.warehouse.capacity())

    # HEALTH

    def regenerate(self, health=20):
        self.health = min(self.health + health, 1000)

    def lower_health(self, health):
        self.health -= health

    # OTHER

    def update_troops(self, army):
        self.warriors = army.get_warriors()
        self.archers = army.get_archers()
        self.catapults = army.get_catapults()

    def add_troops(self, army):
        self.warriors.set_n(self.warriors.get_n() + army.get_warriors().get_n())
        self.archers.set_n(self.archers.get_n() + army.get_archers().get_n())
        self.catapults.set_n(self.catapults.get_n() + army.get_catapults().get_n())

    def get_attack_power(self):
        return (self.warriors.get_attack_power() +
                self.archers.get_attack_power() +
                self.catapults.get_attack_power())

    def get_defense_power(self):
        return (self.warriors.get_defense_power() +
                self.archers.get_defense_power() +
                self.catapults.get_defense_power())

    def __repr__(self):
        string = f"////////// {self.name} \\\\\\\\\\\\\\\\\\\\\n\n"
        string += "******* BUILDINGS *******\n"
        string += f"Barracks level: {self.barracks.get_level()} "
        if self.get_barracks().level == 0:
            string += f"(no troops unlocked; next unlock: Warriors)\n"
        elif self.get_barracks().level == 1:
            string += f"(currently unlocked: Warriors; next unlock: Archers)\n"
        elif self.get_barracks().level == 2:
            string += f"(currently unlocked: Warriors, Archers; next unlock: Catapults)\n"
        else:
            string += "(all troops unlocked)\n"
        string += f"Farm level: {self.farm.get_level()} "
        string += f"(current capacity: {self.farm.capacity()}; with upgrade: {self.farm.next_capacity()})\n"
        string += f"Mine level: {self.mine.get_level()} "
        string += f"(current production rate: {self.mine.production()}; with upgrade: {self.mine.next_production()})\n"
        string += f"Wall level: {self.wall.get_level()} "
        string += f"(current def bonus: {self.wall.defense_bonus()}; with upgrade: {self.wall.next_defense_bonus()})\n"
        string += f"Warehouse level: {self.warehouse.get_level()} "
        string += f"(current capacity: {self.warehouse.capacity()}; with upgrade: {self.warehouse.next_capacity()})\n\n"
        string += "******* TROOPS *******\n"
        string += f"Warriors: {self.warriors.get_n()}\n"
        string += f"Archers: {self.archers.get_n()}\n"
        string += f"Catapults: {self.catapults.get_n()}\n"
        string += f"Total attack power of all troops: {self.get_attack_power()}\n"
        string += f"Total defense power of all troops: {self.get_defense_power()}\n\n"
        string += "******* STATS *******\n"
        string += f"Health: {self.health}/{Village.MAX_HEALTH}\n"
        string += f"Stone: {self.stone}/{self.warehouse.capacity()}"
        return string
