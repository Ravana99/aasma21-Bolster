from agent.reactiveagent import ReactiveAgent, Stance
from game import start_game
from sys import argv


def main():
    if len(argv) != 2:
        raise ValueError("Must pass one and only one command line argument (number of players).")

    n_players = int(argv[1])
    if n_players <= 1:
        raise ValueError("Number of players must be a positive integer greater than 1.")

    play_again = True

    while play_again:
        # 0 = NEUTRAL, 1 = OFFENSIVE, 2 = DEFENSIVE
        agents = [ReactiveAgent(i, Stance(i % 3)) for i in range(n_players)]
        print([agent.stance for agent in agents])
        villages = [agent.get_village() for agent in agents]
        for i, agent in enumerate(agents):
            agent.set_other_villages([village.name for j, village in enumerate(villages) if i != j])

        start_game(agents, villages)

        play_again = input("Play again? (y/n): ") in ("y", "Y")


if __name__ == '__main__':
    main()
