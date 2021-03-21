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

    def __init__(self, i):
        self.name = "Village " + str(i)
        self.barracks = Barracks()
        self.farm = Farm()
        self.mine = Mine()
        self.wall = Wall()
        self.warehouse = Warehouse()
        # TODO: change back to ~1000
        self.health = 10
        self.stone = 100
        self.warriors = Warriors()
        self.archers = Archers()
        self.catapults = Catapults()
        self.was_attacked = False

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

    def was_attacked(self):
        return self.was_attacked

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

    def update_stone(self):
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

    def __repr__(self):
        string = f"////////// {self.name} \\\\\\\\\\\\\\\\\\\\\n"
        string += "******* BUILDINGS *******\n"
        string += f"Barracks level: {self.barracks.get_level()}\n"
        string += f"Farm level: {self.farm.get_level()}\n"
        string += f"Mine level: {self.mine.get_level()}\n"
        string += f"Wall level: {self.wall.get_level()}\n"
        string += f"Warehouse level: {self.warehouse.get_level()}\n"
        string += "******* TROOPS *******\n"
        string += f"Warriors: {self.warriors.get_n()}\n"
        string += f"Archers: {self.archers.get_n()}\n"
        string += f"Catapults: {self.catapults.get_n()}\n"
        string += "******* STATS *******\n"
        string += f"Health: {self.health}\n"
        string += f"Stone: {self.stone}\n"
        string += f"Was attacked: {self.was_attacked}\n"
        return string
