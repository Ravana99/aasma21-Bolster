class InvalidDecisionException(BaseException):
    def __init__(self):
        super().__init__("Invalid decision made. Double check the agent code.")


class Decision:
    """DO NOT INSTANTIATE!"""

    def __init__(self, agent):
        self.agent = agent


class UpgradeDecision(Decision):
    """DO NOT INSTANTIATE!"""

    def execute(self):
        raise NotImplementedError()


class UpgradeBarracksDecision(UpgradeDecision):
    def execute(self):
        return self.agent.upgrade_barracks()


class UpgradeFarmDecision(UpgradeDecision):
    def execute(self):
        return self.agent.upgrade_farm()


class UpgradeMineDecision(UpgradeDecision):
    def execute(self):
        return self.agent.upgrade_mine()


class UpgradeQuarryDecision(UpgradeDecision):
    def execute(self):
        return self.agent.upgrade_quarry()


class UpgradeSawmillDecision(UpgradeDecision):
    def execute(self):
        return self.agent.upgrade_sawmill()


class UpgradeWallDecision(UpgradeDecision):
    def execute(self):
        return self.agent.upgrade_wall()


class UpgradeWarehouseDecision(UpgradeDecision):
    def execute(self):
        return self.agent.upgrade_warehouse()


class UpgradeNothingDecision(UpgradeDecision):
    def execute(self):
        return self.agent.upgrade_nothing()


class RecruitDecision(Decision):
    """DO NOT INSTANTIATE!"""

    def __init__(self, agent, n="1"):
        super().__init__(agent)

        n = self.check(n)
        self.n = n

    def execute(self, n):
        n = self.check(n)
        if n > self.n:
            raise InvalidDecisionException()

    @staticmethod
    def check(n):
        if not (isinstance(n, int) or n.isdigit()):
            raise InvalidDecisionException()
        n = int(n)
        if n < 1:
            raise InvalidDecisionException()
        return n


class RecruitSpiesDecision(RecruitDecision):
    def execute(self, n):
        super().execute(n)
        return self.agent.recruit_spies(n)


class RecruitWarriorsDecision(RecruitDecision):
    def execute(self, n):
        super().execute(n)
        return self.agent.recruit_warriors(n)


class RecruitArchersDecision(RecruitDecision):
    def execute(self, n):
        super().execute(n)
        return self.agent.recruit_archers(n)


class RecruitCatapultsDecision(RecruitDecision):
    def execute(self, n):
        super().execute(n)
        return self.agent.recruit_catapults(n)


class RecruitCavalrymenDecision(RecruitDecision):
    def execute(self, n):
        super().execute(n)
        return self.agent.recruit_cavalrymen(n)


class DemoteSpiesDecision(RecruitDecision):
    def execute(self, n):
        super().execute(n)
        return self.agent.demote_spies(n)


class DemoteWarriorsDecision(RecruitDecision):
    def execute(self, n):
        super().execute(n)
        return self.agent.demote_warriors(n)


class DemoteArchersDecision(RecruitDecision):
    def execute(self, n):
        super().execute(n)
        return self.agent.demote_archers(n)


class DemoteCatapultsDecision(RecruitDecision):
    def execute(self, n):
        super().execute(n)
        return self.agent.demote_catapults(n)


class DemoteCavalrymenDecision(RecruitDecision):
    def execute(self, n):
        super().execute(n)
        return self.agent.demote_cavalrymen(n)


class RecruitNothingDecision(RecruitDecision):
    def execute(self, n=None):
        return self.agent.recruit_nothing()


class SpyingDecision(Decision):
    """DO NOT INSTANTIATE!"""

    enemy_village_name = ""

    def execute(self):
        raise NotImplementedError()


class SpyVillageDecision(SpyingDecision):
    def __init__(self, agent, enemy_village_name):
        super().__init__(agent)
        self.enemy_village_name = enemy_village_name

    def execute(self):
        return self.agent.spy(self.enemy_village_name)


class SpyNothingDecision(SpyingDecision):
    def execute(self):
        return self.agent.spy_nothing()


class AttackDecision(Decision):
    """DO NOT INSTANTIATE!"""

    def __init__(self, agent, n_warriors="0", n_archers="0", n_catapults="0", n_cavalrymen="0", enemy_village_name=""):
        super().__init__(agent)

        n_warriors = self.check(n_warriors)
        self.n_warriors = n_warriors

        n_archers = self.check(n_archers)
        self.n_archers = n_archers

        n_catapults = self.check(n_catapults)
        self.n_catapults = n_catapults

        n_cavalrymen = self.check(n_cavalrymen)
        self.n_cavalrymen = n_cavalrymen

        self.enemy_village_name = enemy_village_name

    def execute(self, n_warriors, n_archers, n_catapults, n_cavalrymen):
        n_warriors = self.check(n_warriors)
        n_archers = self.check(n_archers)
        n_catapults = self.check(n_catapults)
        n_cavalrymen = self.check(n_cavalrymen)

        if n_warriors > self.n_warriors or n_archers > self.n_archers or \
           n_catapults > self.n_catapults or n_cavalrymen > self.n_cavalrymen:
            raise InvalidDecisionException()

        if self.n_warriors + self.n_archers + self.n_catapults + self.n_cavalrymen <= 0:
            raise InvalidDecisionException()

    @staticmethod
    def check(n):
        if not (isinstance(n, int) or n.isdigit()):
            raise InvalidDecisionException()
        n = int(n)
        if n < 0:
            raise InvalidDecisionException()
        return n


class AttackVillageDecision(AttackDecision):
    def __init__(self, agent, n_warriors, n_archers, n_catapults, n_cavalrymen, enemy_village_name):
        super().__init__(agent, n_warriors, n_archers, n_catapults, n_cavalrymen, enemy_village_name)
        if self.n_warriors + self.n_archers + self.n_catapults + self.n_cavalrymen <= 0:
            raise InvalidDecisionException()

    def execute(self, n_warriors, n_archers, n_catapults, n_cavalrymen):
        super().execute(n_warriors, n_archers, n_catapults, n_cavalrymen)
        return self.agent.send_attack(n_warriors, n_archers, n_catapults, n_cavalrymen, self.enemy_village_name)


class AttackNothingDecision(AttackDecision):
    def execute(self, n_warriors=None, n_archers=None, n_catapults=None, n_cavalrymen=None):
        return self.agent.attack_nothing()
