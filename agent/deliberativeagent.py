from agent.agent import Agent
from agent.decisions import *


class DeliberativeAgent(Agent):

    def __init__(self, i):
        super().__init__(i)
        self.desires = []
        self.intention = None
        self.plan = []

    def upgrade_decision(self):
        self.brf()

        while True:
            if self.plan and not self.succeeded_intention() and not self.impossible_intention():
                action = self.plan.pop(0)
                if self.sound():
                    assert issubclass(action.__class__, UpgradeDecision)
                    return action.execute()
                else:
                    self.plan = self.remake_plan()
                if self.reconsider():
                    self.desires = self.options()
                    self.intention = self.filter()

            else:
                self.desires = self.options()
                self.intention = self.filter()
                self.plan = self.make_plan()
                if not self.plan:
                    action = UpgradeNothingDecision(self)
                    assert issubclass(action.__class__, UpgradeDecision)
                    return action.execute()

    @staticmethod
    def brf():
        pass

    @staticmethod
    def options():
        return []

    @staticmethod
    def filter():
        return 0

    @staticmethod
    def make_plan():
        return []

    @staticmethod
    def succeeded_intention():
        return False

    @staticmethod
    def impossible_intention():
        return False

    @staticmethod
    def sound():
        return True

    @staticmethod
    def remake_plan():
        return []

    @staticmethod
    def reconsider():
        return True

    def recruit_decision(self):
        action = RecruitNothingDecision(self)

        assert issubclass(action.__class__, RecruitDecision)
        return action.execute()

    def spying_decision(self):
        action = SpyNothingDecision(self)

        assert issubclass(action.__class__, SpyingDecision)
        return action.execute()

    def attack_decision(self):
        action = AttackNothingDecision(self)

        assert issubclass(action.__class__, AttackDecision)
        return action.execute()
