from agent import Agent


class SpecificAgent(Agent):

    def upgrade_decision(self):
        # TEMPORARY
        self.upgrade_barracks()

    def recruit_decision(self):
        # TEMPORARY
        if self.name == "Agent 0":
            self.recruit_warriors(10)
        else:
            self.recruit_warriors(5)

    def attack_decision(self):
        # TEMPORARY
        if self.name == "Agent 0":
            return self.send_attack(10, 0, 0, "Village 1")
        else:
            return self.attack_nothing()
