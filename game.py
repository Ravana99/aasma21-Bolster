from random import shuffle

agents = []
villages = []


def start_game(agent_list, village_list):
    global agents, villages

    agents = agent_list
    villages = village_list

    turn = 1

    while True:
        print(f"\n\n*************** TURN {turn} ***************\n\n")

        print_player_village()

        for agent in agents:
            agent.upgrade_decision()

        print_player_village()

        for agent in agents:
            agent.recruit_decision()

        print_player_village()

        armies = []
        for agent in agents:
            decision = agent.attack_decision()
            if decision is not None:
                armies.append(decision)

        all_reports = process_attacks(armies)
        return_home(armies, all_reports)

        for report in all_reports:
            winning_village = report.get_winner()
            losing_village = report.get_loser()
            winning_agent = get_agent_by_village_name(winning_village)
            losing_agent = get_agent_by_village_name(losing_village)
            winning_agent.add_report(report)
            losing_agent.add_report(report)

        show_player_reports()

        old_agents = agents.copy()
        eliminate_players()

        if check_winner(old_agents):
            break

        for village in villages:
            village.produce_resources()
            village.regenerate()

        turn += 1


def show_player_reports():
    if agents[0].get_name() == "Player":
        for report in agents[0].get_report_log():
            # Didn't feel like writing dozens of getters for the report...
            if report.new:
                report.set_new(False)
                print()
                print()
                print("~~~~~~~~~~ NEW REPORT ~~~~~~~~~~")
                print()
                print(f"Attacking village: {report.attacking_village} ", end="")
                print(f"({'winner' if report.attacking_village == report.winner else 'loser'})")
                print(f"Defending village: {report.defending_village} ", end="")
                print(f"({'winner' if report.defending_village == report.winner else 'loser'})")
                print(f"Attacking luck: {round(report.attacking_luck, 1)}%")
                print(f"Defending luck: {round(report.defending_luck, 1)}%")
                print(f"Casualty luck: {round(report.casualty_luck, 1)}%")
                print(f"Attacking army at the start (total power: {round(report.attacking_power, 1)}): ", end="")
                print(f"{report.starting_attacking_warriors} warriors, ", end="")
                print(f"{report.starting_attacking_archers} archers, ", end="")
                print(f"{report.starting_attacking_catapults} catapults, ", end="")
                print(f"{report.starting_attacking_cavalrymen} cavalrymen")
                print(f"Defending army at the start (total power: {round(report.defending_power, 1)}): ", end="")
                print(f"{report.starting_defending_warriors} warriors, ", end="")
                print(f"{report.starting_defending_archers} archers, ", end="")
                print(f"{report.starting_defending_catapults} catapults, ", end="")
                print(f"{report.starting_defending_cavalrymen} cavalrymen")
                print(f"Attacking army in the end: ", end="")
                print(f"{report.ending_attacking_warriors} warriors, ", end="")
                print(f"{report.ending_attacking_archers} archers, ", end="")
                print(f"{report.ending_attacking_catapults} catapults, ", end="")
                print(f"{report.ending_attacking_cavalrymen} cavalrymen")
                print(f"Defending army in the end: ", end="")
                print(f"{report.ending_defending_warriors} warriors, ", end="")
                print(f"{report.ending_defending_archers} archers, ", end="")
                print(f"{report.ending_defending_catapults} catapults, ", end="")
                print(f"{report.ending_defending_cavalrymen} cavalrymen")
                print(f"Plundered resources: {report.plundered_resources}")
                print(f"Initial health of defending village: {report.defending_village_health_before}")
                print(f"Damage dealt: {report.damage_dealt}")
                print(f"Current health of defending village: ", end="")
                print(report.defending_village_health_before - report.damage_dealt)
                print()
                print()


def process_attacks(attacking_armies):
    shuffle(attacking_armies)      # Order of attacks is randomized in case of multiple attacks on the same village

    all_reports = []

    for attacking_army in attacking_armies:
        defending_village = get_village_by_name(attacking_army.get_enemy_village_name())
        defending_army = defending_village.create_defensive_army()
        report = attacking_army.attack(defending_army, defending_village.get_wall().defense_bonus())
        plundered_resources = defending_village.plundered(report.get_resources_to_plunder())
        report.set_plundered_resources(plundered_resources)
        report.set_defending_village_health_before(defending_village.get_health())
        all_reports.append(report)
        defending_village.lower_health(report.get_damage_dealt())
        defending_village.update_troops(defending_army)

    return all_reports


def return_home(surviving_armies, all_reports):
    for army, report in zip(surviving_armies, all_reports):
        village = get_village_by_name(army.get_village_name())
        village.add_troops(army)
        village.add_resources(report.get_plundered_resources())


def eliminate_players():
    agents_to_delete = []
    global agents
    for agent in agents:
        if agent.get_village().get_health() <= 0:
            agents_to_delete.append(agent)
            villages.remove(agent.get_village())
            for other_agent in agents:
                if agent != other_agent:
                    other_agent.remove_other_village(agent.get_village().get_name())
    agents = [agent for agent in agents if agent not in agents_to_delete]


def check_winner(old_agents):
    print()
    if len(agents) == 0:
        print("~~~~~~~~~~Tie between players:~~~~~~~~~~")
        for agent in old_agents:
            print(agent.get_name())
        print()
        print()
        return True
    elif len(agents) == 1:
        print("~~~~~~~~~~Winner:~~~~~~~~~~")
        print(agents[0].get_name())
        print()
        print()
        return True
    else:
        return False


def get_village_by_name(name):
    for village in villages:
        if name == village.get_name():
            return village
    return None


def get_agent_by_village_name(name):
    for agent in agents:
        if name == agent.get_village().get_name():
            return agent
    return None


def print_all_villages():
    for village in villages:
        print(village)
    input("\nPress Enter to continue...\n")


def print_player_village():
    print(villages[0])
