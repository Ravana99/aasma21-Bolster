import pickle
from pandas import DataFrame
from collections import Counter
from agent.stance import Stance
from statistics import mean
import numpy as np
import matplotlib.pyplot as plt


n_games = 2500
target = f"bin/outcomes{n_games}dynamic.pickle"
# target = f"bin/outcomes{n_games}static.pickle"


def analyze_data():
    with open(target, "rb") as f:
        print("Unpickling...")
        outcomes = pickle.load(f)
        print("Done!")
        results = [outcome[0] for outcome in outcomes]

        ending_conditions = [result[0] for result in results]

        winners = [result[1] for result in results]

        games = [outcome[1] for outcome in outcomes]

        # How many games ended up in a victory, how many in a tie, how many in a stalemate

        number_of_wins = sum(1 for ending_condition in ending_conditions if ending_condition == "victory")
        number_of_ties = sum(1 for ending_condition in ending_conditions if ending_condition == "tie")
        number_of_stalemates = sum(1 for ending_condition in ending_conditions if ending_condition == "stalemate")
        print(f"Victories: {number_of_wins}")
        print(f"Ties: {number_of_ties}")
        print(f"Stalemates: {number_of_stalemates}")
        print(f"Percentage of victories: {number_of_wins * 100 / n_games}%")
        print(f"Percentage of ties: {number_of_ties * 100 / n_games}%")
        print(f"Percentage of stalemates: {number_of_stalemates * 100 / n_games}%")

        # Analyze ties
        ties = []
        tie_participants = []
        for ending_condition, winner, game in zip(ending_conditions, winners, games):
            if ending_condition == "tie":
                ties.append(game)
                tie_participants.append(winner)

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
        print(f"Percentage of victories won by initially defensive agent: {games_won_by_def * 100 / number_of_wins}%")
        print(f"Percentage of victories won by initially neutral agent: {games_won_by_neut * 100 / number_of_wins}%")
        print(f"Percentage of victories won by initially offensive agent: {games_won_by_off * 100 / number_of_wins}%")

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
        print(f"Percentage of victories won by ending defensive agent: {games_won_by_end_def * 100 / number_of_wins}%")
        print(f"Percentage of victories won by ending neutral agent: {games_won_by_end_neut * 100 / number_of_wins}%")
        print(f"Percentage of victories won by ending offensive agent: {games_won_by_end_off * 100 / number_of_wins}%")

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
        print(f"Percentage of stalemates stalemated by initially defensive agent: "
              f"{games_stale_by_def * 100 / (games_stale_by_def + games_stale_by_neut + games_stale_by_off)}%")
        print(f"Percentage of stalemates stalemated by initially neutral agent: "
              f"{games_stale_by_neut * 100 / (games_stale_by_def + games_stale_by_neut + games_stale_by_off)}%")
        print(f"Percentage of stalemates stalemated by initially offensive agent: "
              f"{games_stale_by_off * 100 / (games_stale_by_def + games_stale_by_neut + games_stale_by_off)}%")

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
        print(f"Percentage of stalemates stalemated by ending defensive agent: "
              f"{games_stale_by_end_def * 100 / (games_stale_by_def + games_stale_by_neut + games_stale_by_off)}%")
        print(f"Percentage of stalemates stalemated by ending neutral agent: "
              f"{games_stale_by_end_neut * 100 / (games_stale_by_def + games_stale_by_neut + games_stale_by_off)}%")
        print(f"Percentage of stalemates stalemated by ending offensive agent: "
              f"{games_stale_by_end_off * 100 / (games_stale_by_def + games_stale_by_neut + games_stale_by_off)}%")

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

        # Percentage of top-half placements
        def_top_half_rank = 0
        neut_top_half_rank = 0
        off_top_half_rank = 0
        for placement in all_placements:
            for game, (agent, rank) in zip(games, placement.items()):
                if game[agent].get_starting_stance() == Stance.DEFENSIVE and rank <= 6.5:
                    def_top_half_rank += 1
                elif game[agent].get_starting_stance() == Stance.NEUTRAL and rank <= 6.5:
                    neut_top_half_rank += 1
                elif game[agent].get_starting_stance() == Stance.OFFENSIVE and rank <= 6.5:
                    off_top_half_rank += 1
        print(f"Top-half placements for defensive agents: {def_top_half_rank}")
        print(f"Top-half placements for neutral agents: {neut_top_half_rank}")
        print(f"Top-half placements for offensive agents: {off_top_half_rank}")
        print(f"Percentage of top-half placements for defensive agents: "
              f"{def_top_half_rank * 100 / (def_top_half_rank + neut_top_half_rank + off_top_half_rank)}%")
        print(f"Percentage of top-half placements for neutral agents: "
              f"{neut_top_half_rank * 100 / (def_top_half_rank + neut_top_half_rank + off_top_half_rank)}%")
        print(f"Percentage of top-half placements for offensive agents: "
              f"{off_top_half_rank * 100 / (def_top_half_rank + neut_top_half_rank + off_top_half_rank)}%")

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

        # Average prosperity ratings
        all_prosp_ratings = []
        all_off_powers = []
        all_def_powers = []
        for ending_condition, winner, game in zip(ending_conditions, winners, games):
            if ending_condition == "victory":
                agent = [agent for agent in game if agent.get_name() == winner[0]][0]
                all_prosp_ratings.append(agent.prosperity_rating_history)
                all_off_powers.append(agent.attack_power_history)
                all_def_powers.append(agent.defense_power_history)

        max_turns = max(lst[-1][1] for lst in all_prosp_ratings)
        all_pad_prosp_ratings = []
        for prosp_rating in all_prosp_ratings:
            ratings = []
            j = 0
            for i in range(1, max_turns + 1):
                ratings.append(prosp_rating[j][0])
                if j == len(prosp_rating) - 1:
                    continue
                elif prosp_rating[j+1][1] == i:
                    j += 1
            all_pad_prosp_ratings.append(ratings)
        mat = np.array(all_pad_prosp_ratings)
        prosp_means_winners = mat.mean(axis=0)

        all_pad_off_powers = []
        for off_power in all_off_powers:
            powers = []
            j = 0
            for i in range(1, max_turns + 1):
                powers.append(off_power[j][0])
                if j == len(off_power) - 1:
                    continue
                elif off_power[j+1][1] == i:
                    j += 1
            all_pad_off_powers.append(powers)
        mat = np.array(all_pad_off_powers)
        off_powers_means_winners = mat.mean(axis=0)

        all_pad_def_powers = []
        for def_power in all_def_powers:
            powers = []
            j = 0
            for i in range(1, max_turns + 1):
                powers.append(def_power[j][0])
                if j == len(def_power) - 1:
                    continue
                elif def_power[j+1][1] == i:
                    j += 1
            all_pad_def_powers.append(powers)
        mat = np.array(all_pad_def_powers)
        def_powers_means_winners = mat.mean(axis=0)

        all_prosp_ratings = []
        all_off_powers = []
        all_def_powers = []

        for ending_condition, winner, game in zip(ending_conditions, winners, games):
            if ending_condition == "victory":
                agents = [agent for agent in game if agent.get_name() != winner[0]]
                for agent in agents:
                    all_prosp_ratings.append(agent.prosperity_rating_history)
                    all_off_powers.append(agent.attack_power_history)
                    all_def_powers.append(agent.defense_power_history)

        max_turns = max(lst[-1][1] for lst in all_prosp_ratings)
        all_pad_prosp_ratings = []
        for prosp_rating in all_prosp_ratings:
            ratings = []
            j = 0
            for i in range(1, max_turns + 1):
                ratings.append(prosp_rating[j][0])
                if j == len(prosp_rating) - 1:
                    continue
                elif prosp_rating[j+1][1] == i:
                    j += 1
            all_pad_prosp_ratings.append(ratings)
        mat = np.array(all_pad_prosp_ratings)
        prosp_means_losers = mat.mean(axis=0)

        all_pad_off_powers = []
        for off_power in all_off_powers:
            powers = []
            j = 0
            for i in range(1, max_turns + 1):
                powers.append(off_power[j][0])
                if j == len(off_power) - 1:
                    continue
                elif off_power[j + 1][1] == i:
                    j += 1
            all_pad_off_powers.append(powers)
        mat = np.array(all_pad_off_powers)
        off_powers_means_losers = mat.mean(axis=0)

        all_pad_def_powers = []
        for def_power in all_def_powers:
            powers = []
            j = 0
            for i in range(1, max_turns + 1):
                powers.append(def_power[j][0])
                if j == len(def_power) - 1:
                    continue
                elif def_power[j + 1][1] == i:
                    j += 1
            all_pad_def_powers.append(powers)
        mat = np.array(all_pad_def_powers)
        def_powers_means_losers = mat.mean(axis=0)

        plt.title("Average prosperity rating per turn in Victory scenarios")
        plt.plot(prosp_means_winners, color='red', label='Winners')
        plt.plot(prosp_means_losers, color='blue', label='Losers')
        plt.xlabel("Turns")
        plt.ylabel("Prosperity rating")
        plt.legend()
        plt.show()

        plt.title("Average offensive power per turn in Victory scenarios")
        plt.plot(off_powers_means_winners, color='red', label='Winners')
        plt.plot(off_powers_means_losers, color='blue', label='Losers')
        plt.xlabel("Turns")
        plt.ylabel("Offensive power")
        plt.legend()
        plt.show()

        plt.title("Average defensive power per turn in Victory scenarios")
        plt.plot(def_powers_means_winners, color='red', label='Winners')
        plt.plot(def_powers_means_losers, color='blue', label='Losers')
        plt.xlabel("Turns")
        plt.ylabel("Defensive power")
        plt.legend()
        plt.show()

        # Total attacks
        successful_attacks = 0
        failed_attacks = 0
        for game in games:
            for agent in game:
                successful_attacks += agent.successful_attacks
                failed_attacks += agent.failed_attacks

        # Turns spent in each stance in total
        all_stances = []
        for game in games:
            for agent in game:
                for i in range(1, agent.get_turn() + 1):
                    all_stances.append(get_current_stance(agent.stance_history, i))
        turns_defensive = sum(1 for stance in all_stances if stance == Stance.DEFENSIVE)
        turns_neutral = sum(1 for stance in all_stances if stance == Stance.NEUTRAL)
        turns_offensive = sum(1 for stance in all_stances if stance == Stance.OFFENSIVE)

        percent_defensive = float(turns_defensive) / (turns_defensive + turns_neutral + turns_offensive)
        percent_neutral = float(turns_neutral) / (turns_defensive + turns_neutral + turns_offensive)
        percent_offensive = float(turns_offensive) / (turns_defensive + turns_neutral + turns_offensive)

        print(f"Percentage of turns spent in defensive stance: {percent_defensive}")
        print(f"Percentage of turns spent in neutral stance: {percent_neutral}")
        print(f"Percentage of turns spent in offensive stance: {percent_offensive}")

        successful_attacks = 0
        failed_attacks = 0
        for ending_condition, winner, game in zip(ending_conditions, winners, games):
            for agent in game:
                successful_attacks += agent.successful_attacks
                failed_attacks += agent.failed_attacks
        print(f"Total successful attacks: {successful_attacks}")
        print(f"Total failed attacks: {failed_attacks}")
        print(f"Percentage of success on attacks: {successful_attacks * 100 / (successful_attacks + failed_attacks)}%")

        def_stance_changes = []
        neut_stance_changes = []
        off_stance_changes = []
        for ending_condition, winner, game in zip(ending_conditions, winners, games):
            for agent in game:
                if agent.get_starting_stance() == Stance.DEFENSIVE:
                    def_stance_changes.append(len(agent.stance_history) - 1)
                elif agent.get_starting_stance() == Stance.NEUTRAL:
                    neut_stance_changes.append(len(agent.stance_history) - 1)
                else:
                    off_stance_changes.append(len(agent.stance_history) - 1)

        avg_def_stance_changes = mean(def_stance_changes)
        avg_neut_stance_changes = mean(neut_stance_changes)
        avg_off_stance_changes = mean(off_stance_changes)
        print(f"Average stance changes per defensive agent per game: {avg_def_stance_changes}")
        print(f"Average stance changes per neutral agent per game: {avg_neut_stance_changes}")
        print(f"Average stance changes per offensive agent per game: {avg_off_stance_changes}")

        return


def get_current_stance(stance_history, current_turn):
    for i, stance in enumerate(stance_history):
        if stance[1] > current_turn:
            return stance_history[i-1][0]
    return stance_history[-1][0]


if __name__ == '__main__':
    analyze_data()
