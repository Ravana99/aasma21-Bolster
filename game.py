from random import shuffle
from copy import deepcopy

# Maximum number of turns per game (if the game reaches this amount of turns, end the game)
TURN_LIMIT = 750

# Maximum number of turns with no players sending out attacks until a stalemate is declared
STALEMATE_LIMIT = 100


agents = []
villages = []


def start_game(agent_list, village_list):
    global agents, villages

    agents = agent_list
    villages = village_list

    turn = 1

    # Stalemate tracker
    turn_of_last_attack = 0

    while turn <= TURN_LIMIT:
        print(f"\n\n*************** TURN {turn} ***************\n\n")

        # Update turn counter for each agent
        for agent in agents:
            agent.set_turn(turn)

        # If a human player is playing, display their village; otherwise, display villages of all agents
        print_villages()

        # Upgrade decision
        for agent in agents:
            agent.upgrade_decision()

        # Recruit decision
        for agent in agents:
            agent.recruit_decision()

        # "New" espionages become "old"
        for agent in agents:
            for espionage in agent.get_spy_log():
                espionage.set_new(False)

        # Spying decision
        spying_missions = []
        for agent in agents:
            decision = agent.spying_decision()
            if decision is not None:
                spying_missions.append(decision)

        # "New" espionages become "old"
        for agent in agents:
            for espionage in agent.get_spy_log():
                espionage.set_new(False)

        # Send out spies and collect espionages
        process_spying(spying_missions, turn)

        # If a human player is playing and they have a new espionage, display it
        if agents[0].get_name() == "Player" and agents[0].get_spy_log() and agents[0].get_spy_log()[0].new:
            print(agents[0].get_spy_log()[0])

        # Attack decision
        armies = []
        for agent in agents:
            decision = agent.attack_decision()
            if decision is not None:
                armies.append(decision)

        # Send out attacks and collect reports
        all_reports = process_attacks(armies, turn)

        # After all attacks are done processing, send surviving troops back to their villages
        return_home(armies, all_reports)

        # If at least one attack was sent, reset stalemate tracker
        if armies:
            turn_of_last_attack = turn

        # "New" reports become "old"
        for agent in agents:
            for report in agent.get_report_log():
                report.set_new(False)

        # Distribute reports
        for report in all_reports:
            winning_village = report.get_winner()
            losing_village = report.get_loser()
            attacking_village = report.get_attacking_village()
            # If attacker lost, don't give that player information regarding the defending troops
            if attacking_village == losing_village:
                truncated_report = deepcopy(report)
                truncated_report.truncate_losing_report()
                winning_agent = get_agent_by_village_name(winning_village)
                losing_agent = get_agent_by_village_name(losing_village)
                winning_agent.add_report(report)
                losing_agent.add_report(truncated_report)
            else:
                winning_agent = get_agent_by_village_name(winning_village)
                losing_agent = get_agent_by_village_name(losing_village)
                winning_agent.add_report(report)
                losing_agent.add_report(report)

        # If a human player is playing, display their new reports
        if agents[0].get_name() == "Player":
            for report in agents[0].get_report_log():
                if report.is_new():
                    print(report)

        # Checks if a stalemate has occurred based on number of turns without agents sending attacks
        if check_stalemate(turn, turn_of_last_attack):
            break

        # Determine players that lost (village dropped to below 0 HP) and check if there is a winner
        old_agents = agents.copy()
        eliminate_players()
        if check_winner(old_agents):
            break

        # Do end-of-turn village updates (produce resources and regenerate health)
        for village in villages:
            village.end_of_turn()

        turn += 1

        print()
        print()

    print()
    print()
    if turn == TURN_LIMIT:
        print("Turn limit reached.")
    else:
        print(f"Game reached {turn - 1} turns.")


def print_villages():
    if agents[0].get_name() == "Player":
        print(villages[0])
    else:
        for village in villages:
            print(village)


def process_spying(spying_missions, turn):
    for mission in spying_missions:
        agent = get_agent_by_village_name(mission.get_village_name())
        # Get deep copy of enemy village for espionage
        enemy_village = deepcopy(get_village_by_name(mission.get_enemy_village_name()))
        mission.set_spied_village(enemy_village)
        mission.set_turn(turn)
        agent.add_espionage(mission)


def process_attacks(attacking_armies, turn):
    # Order of attacks is randomized in case of multiple attacks on the same village
    shuffle(attacking_armies)

    all_reports = []

    # Perform attacks, set missing report attributes, plunder resources and lower village healths
    for attacking_army in attacking_armies:
        defending_village = get_village_by_name(attacking_army.get_enemy_village_name())
        defending_army = defending_village.create_defensive_army()
        report = attacking_army.attack(defending_army, defending_village.get_wall().defense_bonus())
        plundered_resources = defending_village.plundered(report.get_resources_to_plunder())
        report.set_plundered_resources(plundered_resources)
        report.set_defending_village_health_before(defending_village.get_health())
        report.set_turn(turn)
        all_reports.append(report)
        defending_village.lower_health(report.get_damage_dealt())
        defending_village.update_troops(defending_army)

    return all_reports


def return_home(surviving_armies, all_reports):
    for army, report in zip(surviving_armies, all_reports):
        village = get_village_by_name(army.get_village_name())
        village.add_troops(army)
        village.add_resources(report.get_plundered_resources())


def check_stalemate(turn, turn_of_last_attack):
    if turn - turn_of_last_attack > STALEMATE_LIMIT:
        print("~~~~~~~~~~Stalemate between players:~~~~~~~~~~")
        for agent in agents:
            print(agent.get_name())
        print()
        print()
        return True
    return False


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
    # 2+ players simultaneously killed each other - a tie is declared
    if len(agents) == 0:
        print("\n~~~~~~~~~~Tie between players:~~~~~~~~~~")
        for agent in old_agents:
            print(agent.get_name())
        print()
        print()
        return True

    # 1 player left
    elif len(agents) == 1:
        print("\n~~~~~~~~~~Winner:~~~~~~~~~~")
        print(agents[0].get_name())
        print()
        print()
        return True
    else:
        return False


# AUX

def get_village_by_name(name):
    # Village names are unique
    for village in villages:
        if name == village.get_name():
            return village
    return None


def get_agent_by_village_name(name):
    # Village names are unique
    for agent in agents:
        if name == agent.get_village().get_name():
            return agent
    return None
