import pickle


# target = "bin/outcomes100.pickle"
target = "bin/outcomes2500.pickle"


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
        print("ENDING CONDITIONS:")
        print(ending_conditions)
        print("WINNERS:")
        print(winners)
        games = [outcome[1] for outcome in outcomes]
        print("NUMBER OF GAMES:")
        print(len(games))


if __name__ == '__main__':
    analyze_data()
