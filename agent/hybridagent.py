from agent.agent import Agent
from agent.decisions import *


class HybridAgent(Agent):

    def upgrade_decision(self):
        # TODO
        decision = UpgradeNothingDecision(self)

        assert issubclass(decision.__class__, UpgradeDecision)
        return decision.execute()

    def recruit_decision(self):
        # TODO
        decision = RecruitNothingDecision(self)

        assert issubclass(decision.__class__, RecruitDecision)
        return decision.execute()

    def spying_decision(self):
        # TODO
        decision = SpyNothingDecision(self)

        assert issubclass(decision.__class__, SpyingDecision)
        return decision.execute()

    def attack_decision(self):
        # TODO
        decision = AttackNothingDecision(self)

        assert issubclass(decision.__class__, AttackDecision)
        return decision.execute()
