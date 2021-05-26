from agent.reactiveagent import ReactiveAgent, Stance
from game import start_game
from sys import argv
from agent.player import Player


has_player = False


def main():
    global has_player

    if not (len(argv) == 2 or len(argv) == 3):
        raise ValueError("Must pass one or two command line arguments - number of total game participants (2+)"
                         "and, optionally, number of human players (0 or 1).")

    n_players = int(argv[1])
    if n_players <= 1:
        raise ValueError("Number of total game participants must be a positive integer greater than 1.")

    if len(argv) == 2:
        has_player = False
    else:
        humans = int(argv[2])
        if humans == 0:
            has_player = False
        elif humans == 1:
            has_player = True
        else:
            raise ValueError("Number of human players must be either 0 or 1.")

    play_again = True

    while play_again:
        # 0 = NEUTRAL, 1 = OFFENSIVE, 2 = DEFENSIVE
        if has_player:
            agents = [Player(0)]
            agents += [ReactiveAgent(i, Stance(i % 3)) for i in range(1, n_players)]
        else:
            agents = [ReactiveAgent(i, Stance(i % 3)) for i in range(n_players)]
        villages = [agent.get_village() for agent in agents]
        for i, agent in enumerate(agents):
            agent.set_other_villages([village.name for j, village in enumerate(villages) if i != j])

        start_game(agents, villages)

        play_again = input("Play again? (y/n): ") in ("y", "Y")


if __name__ == '__main__':
    main()
