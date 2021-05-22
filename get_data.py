from agent.reactiveagent import ReactiveAgent, Stance
from game import start_game
from copy import deepcopy
import pickle


n_players = 12
n_games = 2500
target = f"bin/outcomes{n_games}dynamic.pickle"


def get_data():
    outcomes = []
    for _ in range(n_games):
        # 0 = NEUTRAL, 1 = OFFENSIVE, 2 = DEFENSIVE
        agents = [ReactiveAgent(i, Stance(i % 3)) for i in range(n_players)]
        villages = [agent.get_village() for agent in agents]
        for i, agent in enumerate(agents):
            agent.set_other_villages([village.name for j, village in enumerate(villages) if i != j])

        winners = start_game(agents, villages)
        winners = deepcopy(winners)
        outcomes.append([winners, deepcopy(agents)])

    with open(target, "wb") as f:
        print("Pickling...")
        pickle.dump(outcomes, f)
        print("Done!")


if __name__ == '__main__':
    get_data()
