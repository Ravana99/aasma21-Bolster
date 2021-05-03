from agent import Agent


class SpecificAgent(Agent):

    upgraded = False

    def upgrade_decision(self):
        # TODO
        return self.upgrade_barracks()
        # return self.upgrade_nothing()

    def recruit_decision(self):
        # TODO
        return self.recruit_warriors(10)
        # return self.recruit_nothing()

    def spying_decision(self):
        # TODO
        return self.spy_nothing()

    def attack_decision(self):
        # TODO
        return self.attack_nothing()
