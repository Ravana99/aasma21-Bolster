from agent import Agent


class SpecificAgent(Agent):

    def upgrade_decision(self):
        # TODO
        # return self.upgrade_nothing()
        return self.upgrade_barracks()

    def recruit_decision(self):
        # TODO
        # return self.recruit_nothing()
        return self.recruit_warriors(5)

    def attack_decision(self):
        # TODO
        return self.attack_nothing()
