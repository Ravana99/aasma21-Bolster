from agent.reactiveagent import ReactiveAgent
from agent.deliberativeagent import DeliberativeAgent
from agent.player import Player
from game import start_game
from sys import argv
from agent.reactiveagent import Stance


def main():
    if len(argv) != 2:
        raise ValueError("Must pass one and only one command line argument (number of players).")

    n_players = int(argv[1])
    if n_players <= 1:
        raise ValueError("Number of players must be a positive integer greater than 1.")

    play_again = True

    while play_again:
        agents = [ReactiveAgent(0, Stance.NEUTRAL),
                  ReactiveAgent(1, Stance.OFFENSIVE),
                  ReactiveAgent(2, Stance.DEFENSIVE)]
        # agents = [DeliberativeAgent(i) if i > 0 else Player(i) for i in range(n_players)]
        villages = [agent.get_village() for agent in agents]
        for i, agent in enumerate(agents):
            agent.set_other_villages([village.name for j, village in enumerate(villages) if i != j])

        start_game(agents, villages)

        play_again = input("Play again? (y/n): ") in ("y", "Y")


if __name__ == '__main__':
    main()
