class Espionage:
    def __init__(self, village_name, enemy_village_name):
        self.village_name = village_name
        self.enemy_village_name = enemy_village_name
        self.spied_village = None
        self.new = True

    def get_village_name(self):
        return self.village_name

    def get_enemy_village_name(self):
        return self.enemy_village_name

    def get_spied_village(self):
        return self.spied_village

    def set_spied_village(self, enemy_village):
        self.spied_village = enemy_village

    def set_new(self, new):
        self.new = new
