from agent import Agent
from troops.warriors import Warriors
from troops.archers import Archers
from troops.catapults import Catapults

from buildings.exceptions import *
from troops.exceptions import *


class Player(Agent):

    def __init__(self, i):
        super().__init__(i)
        self.name = "Player"

    def upgrade_decision(self):
        while True:
            try:
                self.display_upgrade_options()
                selection = input("> ")
                print()
                if selection == "1":
                    return self.upgrade_barracks()
                elif selection == "2":
                    return self.upgrade_farm()
                elif selection == "3":
                    return self.upgrade_mine()
                elif selection == "4":
                    return self.upgrade_wall()
                elif selection == "5":
                    return self.upgrade_warehouse()
                elif selection == "0":
                    return self.upgrade_nothing()
                else:
                    print("Invalid selection. Try again.")

            except UpgradeMaxedOutBuildingException:
                print("Building already maxed out. Try again.")

            except NotEnoughIronToUpgradeException:
                print("Not enough iron to perform upgrade. Try again.")

    def recruit_decision(self):
        while True:
            try:
                self.display_recruitment_options()
                selection = input("> ")
                print()
                if selection == "1":
                    return self.recruit_warriors(input("How many? "))
                elif selection == "2":
                    return self.recruit_archers(input("How many? "))
                elif selection == "3":
                    return self.recruit_catapults(input("How many? "))
                elif selection == "4":
                    return self.demote_warriors(input("How many? "))
                elif selection == "5":
                    return self.demote_archers(input("How many? "))
                elif selection == "6":
                    return self.demote_catapults(input("How many? "))
                elif selection == "0":
                    return self.recruit_nothing()
                else:
                    print("Invalid selection. Try again.")

            except InvalidTroopsToRecruitException:
                print("Invalid number of troops to recruit. Try again.")

            except BarracksLevelTooLowException:
                print("Barracks level too low to recruit that unit. Try again.")

            except NotEnoughFarmCapacityException:
                print("Farm capacity too low to recruit that many units. Try again.")

            except NotEnoughIronToRecruitException:
                print("Not enough iron to recruit that many units. Try again.")

            except InvalidTroopsToDemoteException:
                print("Invalid number of troops to demote. Try again.")

            except TooManyTroopsToDemoteException:
                print("Too many troops to demote. Try again.")

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
                elif selection == 0:
                    return self.attack_nothing()
                else:
                    n_warriors = input("How many warriors? ")
                    n_archers = input("How many archers? ")
                    n_catapults = input("How many catapults? ")
                    return self.send_attack(n_warriors, n_archers, n_catapults, self.other_villages[selection - 1])

            except InvalidTroopsToSendOffException:
                print("Invalid number of troops to send off. Try again.")

            except TooManyTroopsToSendOffException:
                print("Too many troops to send off. Try again.")

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
            print(f"{barracks.get_cost_of_upgrade()} iron)")

        farm = self.get_farm()
        if farm.is_max_level():
            print(f"2: Farm ({farm.get_level()}, maxed out)")
        else:
            print(f"2: Farm ({farm.get_level()}->{farm.get_level() + 1}, ", end="")
            print(f"{farm.get_cost_of_upgrade()} iron)")

        mine = self.get_mine()
        if mine.is_max_level():
            print(f"3: Mine ({mine.get_level()}, maxed out)")
        else:
            print(f"3: Mine ({mine.get_level()}->{mine.get_level() + 1}, ", end="")
            print(f"{mine.get_cost_of_upgrade()} iron)")

        wall = self.get_wall()
        if wall.is_max_level():
            print(f"4: Wall ({wall.get_level()}, maxed out)")
        else:
            print(f"4: Wall ({wall.get_level()}->{wall.get_level() + 1}, ", end="")
            print(f"{wall.get_cost_of_upgrade()} iron)")

        warehouse = self.get_warehouse()
        if warehouse.is_max_level():
            print(f"5: Warehouse ({warehouse.get_level()}, maxed out)")
        else:
            print(f"5: Warehouse ({warehouse.get_level()}->{warehouse.get_level() + 1}, ", end="")
            print(f"{warehouse.get_cost_of_upgrade()} iron)")

        print(f"0: Pass")

    @staticmethod
    def display_recruitment_options():
        print()
        print("What would you like to recruit/demote?")

        print(f"1: (Barracks lvl 1) Recruit warriors ({Warriors.ATTACK} ATK, {Warriors.DEFENSE} DEF, ", end="")
        print(f"{Warriors.COST} iron/unit)")
        print(f"2: (Barracks lvl 2) Recruit archers ({Archers.ATTACK} ATK, {Archers.DEFENSE} DEF, ", end="")
        print(f"{Archers.COST} iron/unit)")
        print(f"3: (Barracks lvl 3) Recruit catapults ({Catapults.ATTACK} ATK, {Catapults.DEFENSE} DEF, ", end="")
        print(f"{Catapults.COST} iron/unit)")
        print(f"4: Demote warriors")
        print(f"5: Demote archers")
        print(f"6: Demote catapults")
        print(f"0: Pass")

    def display_attack_options(self):
        print()
        print("Which village would you like to attack?")
        for i, village in enumerate(self.other_villages):
            print(f"{i + 1}: {village}")
        print("0: Pass")
