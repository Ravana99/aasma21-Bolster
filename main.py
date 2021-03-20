from specificagent import SpecificAgent


n_players = 3


def main():
    agents = [SpecificAgent(i) for i in range(n_players)]
    villages = [agent.get_village() for agent in agents]
    for i, agent in enumerate(agents):
        agent.set_other_villages([village.name for j, village in enumerate(villages) if i != j])

    start_game(agents)


def start_game(agents):
    agent = agents[0]
    village = agent.get_village()
    village.stone = 10000
    village.barracks.level = 2

    print(agent.get_village())

    agent.upgrade_barracks()
    agent.upgrade_farm()
    agent.upgrade_mine()
    agent.upgrade_wall()
    agent.upgrade_warehouse()

    agent.recruit_warriors(4)
    agent.recruit_archers(3)
    agent.recruit_catapults(2)

    agent.demote_warriors(3)
    agent.demote_archers(2)
    agent.demote_catapults(1)

    print(agent.get_village())


if __name__ == '__main__':
    main()
