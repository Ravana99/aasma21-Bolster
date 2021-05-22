import pickle
from pandas import DataFrame
from collections import Counter
from agent.stance import Stance
from statistics import mean


n_games = 100
target = f"bin/outcomes{n_games}dynamic.pickle"
# target = f"bin/outcomes{n_games}static.pickle"


def analyze_data():
    with open(target, "rb") as f:
        print("Unpickling...")
        outcomes = pickle.load(f)
        print("Done!")
        results = [outcome[0] for outcome in outcomes]

        ending_conditions = [result[0] for result in results]

        print(len([cond for cond in ending_conditions if cond == "victory"]))
        print(len([cond for cond in ending_conditions if cond == "stalemate"]))
        print(len([cond for cond in ending_conditions if cond == "tie"]))

        winners = [result[1] for result in results]

        games = [outcome[1] for outcome in outcomes]

        # How many games ended up in a victory, how many in a tie, how many in a stalemate

        number_of_wins = sum(1 for ending_condition in ending_conditions if ending_condition == "victory")
        number_of_ties = sum(1 for ending_condition in ending_conditions if ending_condition == "tie")
        number_of_stalemates = sum(1 for ending_condition in ending_conditions if ending_condition == "stalemate")
        print(f"WINS: {number_of_wins}")
        print(f"TIES: {number_of_ties}")
        print(f"STALEMATES: {number_of_stalemates}")

        # How many agents of each starting stance won a game

        starting_stances = []
        for ending_condition, winner, game in zip(ending_conditions, winners, games):
            winner = winner[0]
            if ending_condition == "victory":
                for agent in game:
                    if agent.get_name() == winner:
                        starting_stances.append(agent.get_starting_stance())

        games_won_by_def = sum(1 for stance in starting_stances if stance == Stance.DEFENSIVE)
        games_won_by_neut = sum(1 for stance in starting_stances if stance == Stance.NEUTRAL)
        games_won_by_off = sum(1 for stance in starting_stances if stance == Stance.OFFENSIVE)
        print(f"Games won by initially defensive agent: {games_won_by_def}")
        print(f"Games won by initially neutral agent: {games_won_by_neut}")
        print(f"Games won by initially offensive agent: {games_won_by_off}")

        # How many agents of each ending stance won a game

        ending_stances = []
        for ending_condition, winner, game in zip(ending_conditions, winners, games):
            winner = winner[0]
            if ending_condition == "victory":
                for agent in game:
                    if agent.get_name() == winner:
                        ending_stances.append(agent.get_ending_stance())

        games_won_by_end_def = sum(1 for stance in ending_stances if stance == Stance.DEFENSIVE)
        games_won_by_end_neut = sum(1 for stance in ending_stances if stance == Stance.NEUTRAL)
        games_won_by_end_off = sum(1 for stance in ending_stances if stance == Stance.OFFENSIVE)
        print(f"Games won by ending defensive agent: {games_won_by_end_def}")
        print(f"Games won by ending neutral agent: {games_won_by_end_neut}")
        print(f"Games won by ending offensive agent: {games_won_by_end_off}")

        # How many agents of each starting stance ended in a stalemate

        starting_stances = []
        for ending_condition, winner, game in zip(ending_conditions, winners, games):
            if ending_condition == "stalemate":
                for agent in game:
                    if agent.get_name() in winner:
                        starting_stances.append(agent.get_starting_stance())

        games_stale_by_def = sum(1 for stance in starting_stances if stance == Stance.DEFENSIVE)
        games_stale_by_neut = sum(1 for stance in starting_stances if stance == Stance.NEUTRAL)
        games_stale_by_off = sum(1 for stance in starting_stances if stance == Stance.OFFENSIVE)
        print(f"Games stalemated by initially defensive agent: {games_stale_by_def}")
        print(f"Games stalemated by initially neutral agent: {games_stale_by_neut}")
        print(f"Games stalemated by initially offensive agent: {games_stale_by_off}")

        # How many agents of each ending stance ended in a stalemate

        ending_stances = []
        for ending_condition, winner, game in zip(ending_conditions, winners, games):
            if ending_condition == "stalemate":
                for agent in game:
                    if agent.get_name() in winner:
                        ending_stances.append(agent.get_ending_stance())

        games_stale_by_end_def = sum(1 for stance in ending_stances if stance == Stance.DEFENSIVE)
        games_stale_by_end_neut = sum(1 for stance in ending_stances if stance == Stance.NEUTRAL)
        games_stale_by_end_off = sum(1 for stance in ending_stances if stance == Stance.OFFENSIVE)
        print(f"Games stalemated by ending defensive agent: {games_stale_by_end_def}")
        print(f"Games stalemated by ending neutral agent: {games_stale_by_end_neut}")
        print(f"Games stalemated by ending offensive agent: {games_stale_by_end_off}")

        # Games lost by ending stance

        ending_stances = []
        for ending_condition, winner, game in zip(ending_conditions, winners, games):
            for agent in game:
                if agent.get_name() not in winner:
                    ending_stances.append(agent.get_ending_stance())

        games_lost_by_end_def = sum(1 for stance in ending_stances if stance == Stance.DEFENSIVE)
        games_lost_by_end_neut = sum(1 for stance in ending_stances if stance == Stance.NEUTRAL)
        games_lost_by_end_off = sum(1 for stance in ending_stances if stance == Stance.OFFENSIVE)
        print(f"Games lost by ending defensive agent: {games_lost_by_end_def}")
        print(f"Games lost by ending neutral agent: {games_lost_by_end_neut}")
        print(f"Games lost by ending offensive agent: {games_lost_by_end_off}")

        # Average placement by starting stance

        all_placements = []
        for ending_condition, winner, game in zip(ending_conditions, winners, games):
            turns_survived = {i: game[i].get_turn() for i in range(len(game))}
            df = DataFrame.from_dict(turns_survived, orient="index")
            df = df.rank(ascending=False)
            placements = df.to_dict(orient="index")
            placements = {key: value[0] for key, value in placements.items()}
            if ending_condition == "victory":
                for key, value in placements.items():
                    if value == 1.5:
                        placements[key] = 1.0 if game[key].get_name() in winner else 2.0
            all_placements.append(placements)
        sums = Counter()
        counters = Counter()
        for item_set in all_placements:
            sums.update(item_set)
            counters.update(item_set.keys())
        avg_placements = {x: float(sums[x]) / counters[x] for x in sums.keys()}
        avg_placements_per_stance = {Stance.NEUTRAL: mean(value for key, value in avg_placements.items()
                                                          if key % 3 == 0),
                                     Stance.OFFENSIVE: mean(value for key, value in avg_placements.items()
                                                            if key % 3 == 1),
                                     Stance.DEFENSIVE: mean(value for key, value in avg_placements.items()
                                                            if key % 3 == 2)}
        print(f"Average placements per starting stance: {avg_placements_per_stance}")

        # Average number of turns per game
        avg_turns_per_game = mean(max(agent.get_turn() for agent in game) for game in games)
        avg_turns_per_victory = mean(max(agent.get_turn() for agent in game)
                                     for ending_condition, game in zip(ending_conditions, games)
                                     if ending_condition == "victory")
        avg_turns_per_stalemate = mean(max(agent.get_turn() for agent in game)
                                       for ending_condition, game in zip(ending_conditions, games)
                                       if ending_condition == "stalemate")

        print(f"Average turns per game: {avg_turns_per_game}")
        print(f"Average turns per victory: {avg_turns_per_victory}")
        print(f"Average turns per stalemate: {avg_turns_per_stalemate}")

        # Stats at turn 90 per starting stance
        all_def_casualties_in_game = []
        all_neut_casualties_in_game = []
        all_off_casualties_in_game = []
        for ending_condition, winner, game in zip(ending_conditions, winners, games):
            def_casualties_in_game = []
            neut_casualties_in_game = []
            off_casualties_in_game = []
            for i, agent in enumerate(game):
                troop_casualties = [x[0] for x in agent.troop_casualties_history if x[1] <= 90]
                troop_casualties = {key: sum(x[key] for x in troop_casualties)
                                    for key in troop_casualties[0].keys()} if len(troop_casualties) > 0 else {}
                if i % 3 == 0:
                    neut_casualties_in_game.append(troop_casualties)
                elif i % 3 == 1:
                    off_casualties_in_game.append(troop_casualties)
                else:
                    def_casualties_in_game.append(troop_casualties)
            for i in range(len(def_casualties_in_game)):
                all_def_casualties_in_game.append(def_casualties_in_game[i])
                all_neut_casualties_in_game.append(neut_casualties_in_game[i])
                all_off_casualties_in_game.append(off_casualties_in_game[i])

        all_avg_casualties = []
        for casualties in (all_neut_casualties_in_game, all_off_casualties_in_game, all_def_casualties_in_game):
            sums = Counter()
            for item_set in casualties:
                sums.update(item_set)
            avg_casualties = {x: float(sums[x]) / (n_games * 12 / 3) for x in sums.keys()}
            all_avg_casualties.append(avg_casualties)
        all_neut_avg_casualties = all_avg_casualties[0]
        all_off_avg_casualties = all_avg_casualties[1]
        all_def_avg_casualties = all_avg_casualties[2]

        print(f"Average casualties per starting defensive agent: {all_def_avg_casualties}")
        print(f"Average casualties per starting neutral agent: {all_neut_avg_casualties}")
        print(f"Average casualties per starting offensive agent: {all_off_avg_casualties}")

        """
        # Average prosperity rating plots for the winner
        for ending_condition, winner, game in zip(ending_conditions, winners, games):
            if ending_condition == "victory":
                agent = [agent for agent in game if agent.get_name() == winner][0]
        """

        return


if __name__ == '__main__':
    analyze_data()
