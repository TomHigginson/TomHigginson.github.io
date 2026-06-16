
import random
import pandas as pd

# ---------------------------
# INPUT TEAMS
# ---------------------------

teams = [
    "Cardiac Arrest",
    "IAC A",
    "IAC AA",
    "Theory FC",
    "Shooting Stars",
    "1/sqrt(2) (|a> + |b>)",
    "Back of the QET",
    "Quantum & Soft Matter"
]

random.shuffle(teams)

# ---------------------------
# SPLIT INTO 2 GROUPS OF 4
# ---------------------------

groupA = teams[:4]
groupB = teams[4:]

# ---------------------------
# ROUND ROBIN (4 TEAMS)
# ---------------------------

def round_robin(group):

    group = list(group)

    n = len(group)
    rounds = []

    for _ in range(n - 1):

        matches = []

        for i in range(n // 2):

            home = group[i]
            away = group[n - 1 - i]

            matches.append((home, away))

        rounds.append(matches)

        # Rotate teams
        group = [group[0]] + [group[-1]] + group[1:-1]

    return rounds

A_rounds = round_robin(groupA)
B_rounds = round_robin(groupB)

# ---------------------------
# BUILD FIXTURES
# ---------------------------

fixtures = []

start_time = 14 * 60
slot = 15

max_rounds = max(len(A_rounds), len(B_rounds))

for r in range(max_rounds):

    A_matches = A_rounds[r]
    B_matches = B_rounds[r]

    max_games = max(len(A_matches), len(B_matches))

    for i in range(max_games):

        # -------------------
        # Lift Side = Group A
        # -------------------

        if i < len(A_matches):

            h, a = A_matches[i]

            fixtures.append([
                "A",
                h,
                "",
                "",
                a
            ])

        # -------------------
        # Clock Side = Group B
        # -------------------

        if i < len(B_matches):

            h, a = B_matches[i]

            fixtures.append([
                "B",
                h,
                "",
                "",
                a
            ])

# ---------------------------
# SAVE CSV
# ---------------------------

df = pd.DataFrame(

    fixtures,

    columns=[
        "Side",
        "Home Team",
        "Home Goals",
        "Away Goals",
        "Away Team"
    ]
)

df.to_csv("fixtures.csv", index=False)

print("Generated Fixtures")
