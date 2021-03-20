from buildings.barracks import Barracks
from buildings.farm import Farm
from buildings.mine import Mine
from buildings.wall import Wall
from buildings.warehouse import Warehouse
from troops.warriors import Warriors
from troops.archers import Archers
from troops.catapults import Catapults


class Village:

    def __init__(self, i):
        self.name = "Village " + str(i)
        self.barracks = Barracks()
        self.farm = Farm()
        self.mine = Mine()
        self.wall = Wall()
        self.warehouse = Warehouse()
        self.health = 1000
        self.stone = 25
        self.warriors = Warriors()
        self.archers = Archers()
        self.catapults = Catapults()
        self.was_attacked = False

    # GETTERS

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

    # STONE

    def update_stone(self):
        stone = self.stone + self.mine.production()
        self.stone = stone if stone < self.warehouse.capacity() else self.warehouse.capacity()

    # OTHER

    def __repr__(self):
        string = ""
        string += f"////////// {self.name} \\\\\\\\\\\\\\\\\\\\\n"
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
