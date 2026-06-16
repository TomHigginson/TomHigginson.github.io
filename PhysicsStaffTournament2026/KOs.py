import pandas as pd

# ---------------------------
# LOAD FIXTURES
# ---------------------------

df = pd.read_csv("fixtures.csv")


# ---------------------------
# BUILD STANDINGS
# ---------------------------

def build_standings(group):

    teams = {}

    group_df = df[df["Side"] == group]

    for _, m in group_df.iterrows():

        h = m["Home Team"]
        a = m["Away Team"]

        if pd.isna(h) or pd.isna(a):
            continue

        hs = m["Home Goals"]
        as_ = m["Away Goals"]

        if pd.isna(hs) or pd.isna(as_):
            continue

        hs = int(hs)
        as_ = int(as_)

        for t in [h, a]:
            if t not in teams:
                teams[t] = {"W":0,"D":0,"L":0,"GF":0,"GA":0,"Pts":0}

        teams[h]["GF"] += hs
        teams[h]["GA"] += as_

        teams[a]["GF"] += as_
        teams[a]["GA"] += hs

        if hs > as_:
            teams[h]["W"] += 1
            teams[a]["L"] += 1
            teams[h]["Pts"] += 3

        elif as_ > hs:
            teams[a]["W"] += 1
            teams[h]["L"] += 1
            teams[a]["Pts"] += 3

        else:
            teams[h]["D"] += 1
            teams[a]["D"] += 1
            teams[h]["Pts"] += 1
            teams[a]["Pts"] += 1

    table = []

    for t,v in teams.items():
        table.append({
            "Team": t,
            "Pts": v["Pts"],
            "GD": v["GF"] - v["GA"],
            "GF": v["GF"]
        })

    table.sort(key=lambda x: (x["Pts"], x["GD"], x["GF"]), reverse=True)

    return [x["Team"] for x in table]


# ---------------------------
# SAFE PICK FUNCTION
# ---------------------------

def safe_get(lst, idx, fallback):
    if idx < len(lst):
        return lst[idx]
    return fallback


# ---------------------------
# GET GROUPS
# ---------------------------

A = build_standings("A")
B = build_standings("B")

# ensure length 5 with placeholders
while len(A) < 5: A.append(None)
while len(B) < 5: B.append(None)


def A_pos(i):
    return A[i] if A[i] else f"Group A Position {i+1}"

def B_pos(i):
    return B[i] if B[i] else f"Group B Position {i+1}"


# ---------------------------
# ASSIGN POSITIONS
# ---------------------------

A1, A2, A3, A4, A5 = A_pos(0), A_pos(1), A_pos(2), A_pos(3), A_pos(4)
B1, B2, B3, B4, B5 = B_pos(0), B_pos(1), B_pos(2), B_pos(3), B_pos(4)


# ---------------------------
# BUILD FIXTURES
# ---------------------------

fixtures = []

# ---------------- Semi Finals ----------------
fixtures += [
    ["A","Europa League","Semi Final", A3, B4],
    ["B","Europa League","Semi Final", B3, A4],
    ["A","Champions League","Semi Final", A1, B2],
    ["B","Champions League","Semi Final", B1, A2]
]

# ---------------- Third Place ----------------
fixtures += [
    ["A","Europa League","3rd Place","TBD","TBD"],
    ["B","Champions League","3rd Place","TBD","TBD"],
]

# ---------------- Major Finals ----------------
fixtures += [
    ["A","Conference League","Final", A5, B5],
    ["B","Europa League","Final","TBD","TBD"],
    ["B","Champions League","Final","TBD","TBD"]
]


# ---------------------------
# SAVE
# ---------------------------

out = pd.DataFrame(fixtures, columns=["Side","Competition","Stage","Team1","Team2"])
out.to_csv("knockouts.csv", index=False)

print("Knockouts generated with safe placeholders")