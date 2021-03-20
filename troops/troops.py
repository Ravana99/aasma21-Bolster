class Troops:
    n = 0
    attack = -1
    defense = -1
    cost = -1
    min_level = -1

    def get_n(self):
        return self.n

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def get_cost(self):
        return self.cost

    def recruit(self, stone, n, level, free_capacity):
        if level < self.min_level:
            raise Exception("Barracks level too low to recruit these troops")
        elif n > free_capacity:
            raise Exception("Not enough farm capacity to recruit these troops")
        elif self.cost * n > stone:
            raise Exception("Not enough stone to recruit that many troops")
        else:
            stone = stone - self.cost * n
            self.n += n
            return stone

    def demote(self, n):
        if n > self.n:
            raise Exception("Troops to demote are greater than the current number of troops")
        self.n -= n
