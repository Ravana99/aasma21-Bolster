from buildings.barracks import Barracks
from buildings.farm import Farm
from buildings.mine import Mine
from buildings.quarry import Quarry
from buildings.sawmill import Sawmill
from buildings.wall import Wall
from buildings.warehouse import Warehouse
from troops.espionage import Espionage
from troops.spies import Spies
from troops.warriors import Warriors
from troops.archers import Archers
from troops.catapults import Catapults
from troops.cavalrymen import Cavalrymen
from troops.army import Army
from troops.exceptions import InvalidTroopsToSendOffException


class Village:

    MAX_HEALTH = 10000
    STARTING_RESOURCES = 100

    def __init__(self, i):
        self.name = "Village " + str(i)
        self.barracks = Barracks()
        self.farm = Farm()
        self.mine = Mine()
        self.quarry = Quarry()
        self.sawmill = Sawmill()
        self.wall = Wall()
        self.warehouse = Warehouse()
        self.health = Village.MAX_HEALTH
        self.iron = Village.STARTING_RESOURCES
        self.stone = Village.STARTING_RESOURCES
        self.wood = Village.STARTING_RESOURCES
        self.spies = Spies()
        self.warriors = Warriors()
        self.archers = Archers()
        self.catapults = Catapults()
        self.cavalrymen = Cavalrymen()

    # GETTERS

    def get_name(self):
        return self.name

    def get_barracks(self):
        return self.barracks

    def get_farm(self):
        return self.farm

    def get_mine(self):
        return self.mine

    def get_quarry(self):
        return self.quarry

    def get_sawmill(self):
        return self.sawmill

    def get_wall(self):
        return self.wall

    def get_warehouse(self):
        return self.warehouse

    def get_all_buildings(self):
        return [self.barracks, self.farm, self.mine, self.quarry, self.sawmill, self.wall, self.warehouse]

    def get_health(self):
        return self.health

    def get_iron(self):
        return self.iron

    def get_stone(self):
        return self.stone

    def get_wood(self):
        return self.wood

    def get_spies(self):
        return self.spies

    def get_warriors(self):
        return self.warriors

    def get_archers(self):
        return self.archers

    def get_catapults(self):
        return self.catapults

    def get_cavalrymen(self):
        return self.cavalrymen

    def get_troops(self):
        return self.spies.get_n() + self.warriors.get_n() + self.archers.get_n() + \
               self.catapults.get_n() + self.cavalrymen.get_n()

    def get_prosperity_rating(self):
        return sum(2 ** building.get_level() for building in self.get_all_buildings())

    # UPGRADES

    def upgrade_barracks(self):
        self.iron, self.stone, self.wood = self.barracks.upgrade(self.iron, self.stone, self.wood)

    def upgrade_farm(self):
        self.iron, self.stone, self.wood = self.farm.upgrade(self.iron, self.stone, self.wood)

    def upgrade_mine(self):
        self.iron, self.stone, self.wood = self.mine.upgrade(self.iron, self.stone, self.wood)

    def upgrade_quarry(self):
        self.iron, self.stone, self.wood = self.quarry.upgrade(self.iron, self.stone, self.wood)

    def upgrade_sawmill(self):
        self.iron, self.stone, self.wood = self.sawmill.upgrade(self.iron, self.stone, self.wood)

    def upgrade_wall(self):
        self.iron, self.stone, self.wood = self.wall.upgrade(self.iron, self.stone, self.wood)

    def upgrade_warehouse(self):
        self.iron, self.stone, self.wood = self.warehouse.upgrade(self.iron, self.stone, self.wood)

    # RECRUITMENTS

    def recruit_spies(self, n):
        free_capacity = self.farm.capacity() - self.get_troops()
        self.iron, self.stone, self.wood = self.spies.recruit(self.iron, self.stone, self.wood,
                                                              n, self.barracks.get_level(), free_capacity)

    def recruit_warriors(self, n):
        free_capacity = self.farm.capacity() - self.get_troops()
        self.iron, self.stone, self.wood = self.warriors.recruit(self.iron, self.stone, self.wood,
                                                                 n, self.barracks.get_level(), free_capacity)

    def recruit_archers(self, n):
        free_capacity = self.farm.capacity() - self.get_troops()
        self.iron, self.stone, self.wood = self.archers.recruit(self.iron, self.stone, self.wood,
                                                                n, self.barracks.get_level(), free_capacity)

    def recruit_catapults(self, n):
        free_capacity = self.farm.capacity() - self.get_troops()
        self.iron, self.stone, self.wood = self.catapults.recruit(self.iron, self.stone, self.wood,
                                                                  n, self.barracks.get_level(), free_capacity)

    def recruit_cavalrymen(self, n):
        free_capacity = self.farm.capacity() - self.get_troops()
        self.iron, self.stone, self.wood = self.cavalrymen.recruit(self.iron, self.stone, self.wood,
                                                                   n, self.barracks.get_level(), free_capacity)

    def demote_spies(self, n):
        self.spies.demote(n)

    def demote_warriors(self, n):
        self.warriors.demote(n)

    def demote_archers(self, n):
        self.archers.demote(n)

    def demote_catapults(self, n):
        self.catapults.demote(n)

    def demote_cavalrymen(self, n):
        self.cavalrymen.demote(n)

    # SPYING

    def spy(self, enemy_village_name):
        self.spies.send_off(1)
        return Espionage(self.name, enemy_village_name)

    # ATTACKS

    def create_attacking_army(self, n_warriors, n_archers, n_catapults, n_cavalrymen, enemy_village_name):
        self.send_off(n_warriors, n_archers, n_catapults, n_cavalrymen)
        return Army(n_warriors, n_archers, n_catapults, n_cavalrymen,
                    self.name, enemy_village_name=enemy_village_name, attacking=True)

    def create_defensive_army(self):
        return Army(self.warriors.get_n(), self.archers.get_n(), self.catapults.get_n(), self.cavalrymen.get_n(),
                    self.name, attacking=False)

    # RESOURCES

    def add_resources(self, resources):
        self.add_iron(resources[0])
        self.add_stone(resources[1])
        self.add_wood(resources[2])

    def remove_resources(self, resources):
        self.remove_iron(resources[0])
        self.remove_stone(resources[1])
        self.remove_wood(resources[2])

    def produce_resources(self):
        self.produce_iron()
        self.produce_stone()
        self.produce_wood()

    # IRON

    def add_iron(self, iron):
        self.iron = min(self.iron + iron, self.warehouse.capacity())

    def remove_iron(self, iron):
        self.iron = max(self.iron - iron, 0)

    def produce_iron(self):
        self.iron = min(self.iron + self.mine.production(), self.warehouse.capacity())

    # STONE

    def add_stone(self, stone):
        self.stone = min(self.stone + stone, self.warehouse.capacity())

    def remove_stone(self, stone):
        self.stone = max(self.stone - stone, 0)

    def produce_stone(self):
        self.stone = min(self.stone + self.quarry.production(), self.warehouse.capacity())

    # WOOD

    def add_wood(self, wood):
        self.wood = min(self.wood + wood, self.warehouse.capacity())

    def remove_wood(self, wood):
        self.wood = max(self.wood - wood, 0)

    def produce_wood(self):
        self.wood = min(self.wood + self.sawmill.production(), self.warehouse.capacity())

    # HEALTH

    def regenerate(self, health=100):
        self.health = min(self.health + health, Village.MAX_HEALTH)

    def lower_health(self, health):
        self.health -= health

    # OTHER

    def end_of_turn(self):
        self.produce_resources()
        self.regenerate()

    def send_off(self, n_warriors, n_archers, n_catapults, n_cavalrymen):
        original_warriors, original_archers, original_catapults, original_cavalrymen = \
            self.warriors.get_n(), self.archers.get_n(), self.catapults.get_n(), self.cavalrymen.get_n()
        try:
            self.warriors.send_off(n_warriors)
            self.archers.send_off(n_archers)
            self.catapults.send_off(n_catapults)
            self.cavalrymen.send_off(n_cavalrymen)
        except InvalidTroopsToSendOffException:
            self.warriors.set_n(original_warriors)
            self.archers.set_n(original_archers)
            self.catapults.set_n(original_catapults)
            self.cavalrymen.set_n(original_cavalrymen)
            raise InvalidTroopsToSendOffException()

    def update_troops(self, army):
        self.warriors = army.get_warriors()
        self.archers = army.get_archers()
        self.catapults = army.get_catapults()
        self.cavalrymen = army.get_cavalrymen()

    def add_troops(self, army):
        self.warriors.set_n(self.warriors.get_n() + army.get_warriors().get_n())
        self.archers.set_n(self.archers.get_n() + army.get_archers().get_n())
        self.catapults.set_n(self.catapults.get_n() + army.get_catapults().get_n())
        self.cavalrymen.set_n(self.cavalrymen.get_n() + army.get_cavalrymen().get_n())

    def get_attack_power(self):
        return (self.warriors.get_attack_power() +
                self.archers.get_attack_power() +
                self.catapults.get_attack_power() +
                self.cavalrymen.get_attack_power())

    def get_attack_power_no_archers(self):
        return (self.warriors.get_attack_power() +
                self.catapults.get_attack_power() +
                self.cavalrymen.get_attack_power())

    def get_defense_power(self):
        return self.wall.defense_bonus() * \
               (self.warriors.get_defense_power() +
                self.archers.get_defense_power() +
                self.catapults.get_defense_power() +
                self.cavalrymen.get_defense_power())

    def plundered(self, amount):
        stolen_iron = min(self.iron, amount)
        stolen_stone = min(self.stone, amount)
        stolen_wood = min(self.wood, amount)
        stolen_resources = [stolen_iron, stolen_stone, stolen_wood]
        self.remove_resources(stolen_resources)
        return stolen_resources

    def __repr__(self):
        string = f"////////// {self.name} \\\\\\\\\\\\\\\\\\\\\n\n"
        string += "******* BUILDINGS *******\n"
        string += f"Barracks level: {self.barracks.get_level()} "
        if self.get_barracks().level == 0:
            string += f"(no troops unlocked; next unlock: Spies, Warriors)\n"
        elif self.get_barracks().level == 1:
            string += f"(currently unlocked: Spies, Warriors; next unlock: Archers, Catapults)\n"
        elif self.get_barracks().level == 2:
            string += f"(currently unlocked: Spies, Warriors, Archers, Catapults; next unlock: Cavalrymen)\n"
        else:
            string += "(all troops unlocked)\n"
        string += f"Farm level: {self.farm.get_level()} "
        string += f"(current capacity: {self.farm.capacity()}; upgrade: {self.farm.next_capacity()})\n"
        string += f"Mine level: {self.mine.get_level()} "
        string += f"(current production rate: {self.mine.production()}; upgrade: {self.mine.next_production()})\n"
        string += f"Quarry level: {self.quarry.get_level()} "
        string += f"(current production rate: {self.quarry.production()}; upgrade: {self.quarry.next_production()})\n"
        string += f"Sawmill level: {self.sawmill.get_level()} "
        string += f"(current production rate: {self.sawmill.production()}; upgrade: {self.sawmill.next_production()})\n"
        string += f"Wall level: {self.wall.get_level()} "
        string += f"(current def bonus: {self.wall.defense_bonus()}; upgrade: {self.wall.next_defense_bonus()})\n"
        string += f"Warehouse level: {self.warehouse.get_level()} "
        string += f"(current capacity: {self.warehouse.capacity()}; upgrade: {self.warehouse.next_capacity()})\n\n"
        string += "******* TROOPS *******\n"
        string += f"Spies: {self.spies.get_n()}\n"
        string += f"Warriors: {self.warriors.get_n()}\n"
        string += f"Archers: {self.archers.get_n()}\n"
        string += f"Catapults: {self.catapults.get_n()}\n"
        string += f"Cavalrymen: {self.cavalrymen.get_n()}\n"
        string += f"Total troops: {self.get_troops()}/{self.farm.capacity()}\n"
        string += f"Total attack power of all troops: {self.get_attack_power()}\n"
        string += f"Total defense power of all troops: {self.get_defense_power()}\n\n"
        string += "******* STATS *******\n"
        string += f"Health: {self.health}/{Village.MAX_HEALTH}\n"
        string += f"Iron: {self.iron}/{self.warehouse.capacity()}\n"
        string += f"Stone: {self.stone}/{self.warehouse.capacity()}\n"
        string += f"Wood: {self.wood}/{self.warehouse.capacity()}"
        return string
