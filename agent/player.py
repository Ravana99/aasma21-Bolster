from agent.agent import Agent
from agent.decisions import *
from troops.spies import Spies
from troops.warriors import Warriors
from troops.archers import Archers
from troops.catapults import Catapults
from troops.cavalrymen import Cavalrymen

from buildings.exceptions import *
from troops.exceptions import *


class Player(Agent):

    def __init__(self, i):
        super().__init__(i)
        self.name = "Player"

    def upgrade_decision(self):
        self.update_state()  # TODO: needed?
        while True:
            self.display_upgrade_options()
            selection = input("> ")
            print()
            if selection == "1":
                decision = UpgradeBarracksDecision(self)
            elif selection == "2":
                decision = UpgradeFarmDecision(self)
            elif selection == "3":
                decision = UpgradeMineDecision(self)
            elif selection == "4":
                decision = UpgradeQuarryDecision(self)
            elif selection == "5":
                decision = UpgradeSawmillDecision(self)
            elif selection == "6":
                decision = UpgradeWallDecision(self)
            elif selection == "7":
                decision = UpgradeWarehouseDecision(self)
            elif selection == "0":
                decision = UpgradeNothingDecision(self)
            else:
                print("Invalid selection. Try again.")
                continue

            try:
                assert issubclass(decision.__class__, UpgradeDecision)
                return decision.execute()
            except UpgradeMaxedOutBuildingException:
                print("Building already maxed out. Try again.")
            except NotEnoughResourcesToUpgradeException:
                print("Not enough resources to perform upgrade. Try again.")

    def recruit_decision(self):
        while True:
            try:
                self.display_recruitment_options()
                selection = input("> ")
                print()
                if selection == "1":
                    decision = RecruitSpiesDecision(self, input("How many? "))
                elif selection == "2":
                    decision = RecruitWarriorsDecision(self, input("How many? "))
                elif selection == "3":
                    decision = RecruitArchersDecision(self, input("How many? "))
                elif selection == "4":
                    decision = RecruitCatapultsDecision(self, input("How many? "))
                elif selection == "5":
                    decision = RecruitCavalrymenDecision(self, input("How many? "))
                elif selection == "6":
                    decision = DemoteSpiesDecision(self, input("How many? "))
                elif selection == "7":
                    decision = DemoteWarriorsDecision(self, input("How many? "))
                elif selection == "8":
                    decision = DemoteArchersDecision(self, input("How many? "))
                elif selection == "9":
                    decision = DemoteCatapultsDecision(self, input("How many? "))
                elif selection == "10":
                    decision = DemoteCavalrymenDecision(self, input("How many? "))
                elif selection == "0":
                    decision = RecruitNothingDecision(self)
                else:
                    print("Invalid selection. Try again.")
                    continue

                assert issubclass(decision.__class__, RecruitDecision)
                return decision.execute(decision.n)

            except InvalidDecisionException:
                print("Invalid decision. Try again.")
            except InvalidTroopsToRecruitException:
                print("Invalid number of troops to recruit. Try again.")
            except BarracksLevelTooLowException:
                print("Barracks level too low to recruit that unit. Try again.")
            except NotEnoughFarmCapacityException:
                print("Farm capacity too low to recruit that many units. Try again.")
            except NotEnoughResourcesToRecruitException:
                print("Not enough resources to recruit that many units. Try again.")
            except InvalidTroopsToDemoteException:
                print("Invalid number of troops to demote. Try again.")
            except TooManyTroopsToDemoteException:
                print("Too many troops to demote. Try again.")

    def spying_decision(self):
        while True:
            self.display_spying_options()
            selection = input("> ")
            print()
            if not (isinstance(selection, int) or selection.isdigit()):
                print("Invalid selection. Try again.")
                continue
            selection = int(selection)
            if selection < 0 or selection > len(self.other_villages):
                print("Invalid selection. Try again.")
                continue
            elif selection == 0:
                decision = SpyNothingDecision(self)
            else:
                decision = SpyVillageDecision(self, self.other_villages[selection - 1])

            try:
                assert issubclass(decision.__class__, SpyingDecision)
                return decision.execute()
            except InvalidTroopsToSendOffException:
                print("No spies available. Try again.")

    def attack_decision(self):
        while True:
            try:
                self.display_attack_options()
                selection = input("> ")
                print()
                if not (isinstance(selection, int) or selection.isdigit()):
                    print("Invalid selection. Try again.")
                    continue
                selection = int(selection)
                if selection < 0 or selection > len(self.other_villages):
                    print("Invalid selection. Try again.")
                    continue
                elif selection == 0:
                    decision = AttackNothingDecision(self)
                else:
                    n_warriors = input("How many warriors? ")
                    n_archers = input("How many archers? ")
                    n_catapults = input("How many catapults? ")
                    n_cavalrymen = input("How many cavalrymen? ")
                    decision = AttackVillageDecision(self, n_warriors, n_archers, n_catapults, n_cavalrymen,
                                                     self.other_villages[selection - 1])

                assert issubclass(decision.__class__, AttackDecision)
                return decision.execute(decision.n_warriors, decision.n_archers,
                                        decision.n_catapults, decision.n_cavalrymen)

            except InvalidDecisionException:
                print("Invalid decision. Try again.")
            except InvalidTroopsToSendOffException:
                print("Invalid number of troops to send off. Try again.")
            except AttackWithNoArmyException:
                print("Cannot attack with no troops. Try again.")

    def display_upgrade_options(self):
        print()
        print("What would you like to upgrade?")

        barracks = self.get_barracks()
        if barracks.is_max_level():
            print(f"1: Barracks ({barracks.get_level()}, maxed out)")
        else:
            print(f"1: Barracks ({barracks.get_level()}->{barracks.get_level() + 1}, ", end="")
            print(f"{barracks.get_cost_of_upgrade()} resources)")

        farm = self.get_farm()
        if farm.is_max_level():
            print(f"2: Farm ({farm.get_level()}, maxed out)")
        else:
            print(f"2: Farm ({farm.get_level()}->{farm.get_level() + 1}, ", end="")
            print(f"{farm.get_cost_of_upgrade()} resources)")

        mine = self.get_mine()
        if mine.is_max_level():
            print(f"3: Mine ({mine.get_level()}, maxed out)")
        else:
            print(f"3: Mine ({mine.get_level()}->{mine.get_level() + 1}, ", end="")
            print(f"{mine.get_cost_of_upgrade()} resources)")

        quarry = self.get_quarry()
        if quarry.is_max_level():
            print(f"4: Quarry ({quarry.get_level()}, maxed out)")
        else:
            print(f"4: Quarry ({quarry.get_level()}->{quarry.get_level() + 1}, ", end="")
            print(f"{quarry.get_cost_of_upgrade()} resources)")

        sawmill = self.get_sawmill()
        if sawmill.is_max_level():
            print(f"5: Sawmill ({sawmill.get_level()}, maxed out)")
        else:
            print(f"5: Sawmill ({sawmill.get_level()}->{sawmill.get_level() + 1}, ", end="")
            print(f"{sawmill.get_cost_of_upgrade()} resources)")

        wall = self.get_wall()
        if wall.is_max_level():
            print(f"6: Wall ({wall.get_level()}, maxed out)")
        else:
            print(f"6: Wall ({wall.get_level()}->{wall.get_level() + 1}, ", end="")
            print(f"{wall.get_cost_of_upgrade()} resources)")

        warehouse = self.get_warehouse()
        if warehouse.is_max_level():
            print(f"7: Warehouse ({warehouse.get_level()}, maxed out)")
        else:
            print(f"7: Warehouse ({warehouse.get_level()}->{warehouse.get_level() + 1}, ", end="")
            print(f"{warehouse.get_cost_of_upgrade()} resources)")

        print(f"0: Pass")

    @staticmethod
    def display_recruitment_options():
        print()
        print("What would you like to recruit/demote?")

        print(f"1: (Barracks lvl {Warriors.MIN_BARRACKS_LEVEL}) Recruit spies ({Spies.COST} resources/unit)")
        print(f"2: (Barracks lvl {Warriors.MIN_BARRACKS_LEVEL}) Recruit warriors ", end="")
        print(f"({Warriors.ATTACK} ATK, {Warriors.DEFENSE} DEF, {Warriors.COST} resources/unit)")
        print(f"3: (Barracks lvl {Archers.MIN_BARRACKS_LEVEL}) Recruit archers ", end="")
        print(f"({Archers.ATTACK} ATK, {Archers.DEFENSE} DEF, {Archers.COST} resources/unit)")
        print(f"4: (Barracks lvl {Catapults.MIN_BARRACKS_LEVEL}) Recruit catapults ", end="")
        print(f"({Catapults.ATTACK} ATK, {Catapults.DEFENSE} DEF, {Catapults.COST} resources/unit)")
        print(f"5: (Barracks lvl {Cavalrymen.MIN_BARRACKS_LEVEL}) Recruit cavalrymen ", end="")
        print(f"({Cavalrymen.ATTACK} ATK, {Cavalrymen.DEFENSE} DEF, {Cavalrymen.COST} resources/unit)")
        print(f"6: Demote spies")
        print(f"7: Demote warriors")
        print(f"8: Demote archers")
        print(f"9: Demote catapults")
        print(f"10: Demote cavalrymen")
        print(f"0: Pass")

    def display_spying_options(self):
        print()
        print("Which village would you like to spy?")
        for i, village in enumerate(self.other_villages):
            print(f"{i + 1}: {village}")
        print("0: Pass")

    def display_attack_options(self):
        print()
        print("Which village would you like to attack?")
        for i, village in enumerate(self.other_villages):
            print(f"{i + 1}: {village}")
        print("0: Pass")
