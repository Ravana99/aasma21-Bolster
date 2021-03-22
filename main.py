from specificagent import SpecificAgent
from player import Player
from random import shuffle


n_players = 2
agents = []
villages = []


def main():
    play_again = True

    while play_again:
        global agents, villages
        agents = [SpecificAgent(i) if i > 0 else Player(i) for i in range(n_players)]
        villages = [agent.get_village() for agent in agents]
        for i, agent in enumerate(agents):
            agent.set_other_villages([village.name for j, village in enumerate(villages) if i != j])

        start_game()
        play_again = input("Play again? (y/n): ") in ("y", "Y")


def start_game():
    turn = 1

    while True:
        print(f"\n\n*************** TURN {turn} ***************\n\n")

        debug_print()

        for agent in agents:
            agent.upgrade_decision()

        debug_print()

        for agent in agents:
            agent.recruit_decision()

        debug_print()

        armies = []
        for agent in agents:
            decision = agent.attack_decision()
            if decision is not None:
                armies.append(decision)

        process_attacks(armies)

        debug_print()

        return_home(armies)

        debug_print()

        old_agents = agents.copy()
        eliminate_players()

        if check_winner(old_agents):
            break

        for village in villages:
            village.update_stone()
            village.regenerate()

        debug_print()

        turn += 1


def process_attacks(attacking_armies):
    shuffle(attacking_armies)      # Order of attacks is randomized in case of multiple attacks on the same village

    for attacking_army in attacking_armies:
        defending_village = get_village_by_name(attacking_army.get_enemy_village_name())
        defending_army = defending_village.create_defensive_army()
        damage_dealt = attacking_army.attack(defending_army, defending_village.get_wall().defense_bonus())
        defending_village.lower_health(damage_dealt)
        defending_village.update_troops(defending_army)


def return_home(surviving_armies):
    for army in surviving_armies:
        village = get_village_by_name(army.get_village_name())
        village.add_troops(army)


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


def debug_print():
    print(villages[0])
    # for village in villages:
    # print(village)
    # input("\nPress Enter to continue...\n")


if __name__ == '__main__':
    main()
