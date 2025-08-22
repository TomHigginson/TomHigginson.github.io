import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

ZONES = {
    "Premier League": [(1, 4), (5, 7), (8, 12), (13, 17), (18, 20)],
    "Championship": [(1, 2), (3, 6), (7, 12), (13, 17), (18, 21), (22, 24)],
}

BBC_URLS = {
    "Premier League": "https://www.bbc.com/sport/football/premier-league/table",
    "Championship": "https://www.bbc.com/sport/football/championship/table",
}

def get_zone(pos, league):
    """
    Sets up the zone reegions for the scoring - to edit please look at 
    the first lines of the code.
    """
    for i, (start, end) in enumerate(ZONES[league]):
        if start <= pos <= end:
            return i
    return -1

def scrape_table(league):
    """
    Takes the live tables from the BBC - the code will fail here if the URL changes.
    """
    url = BBC_URLS[league]
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    rows = soup.select("table tbody tr")

    table = []
    for i, row in enumerate(rows, start=1):
        cols = row.find_all("td")
        if len(cols) < 10:
            # not table; skip
            continue
        raw_team = cols[0].get_text(strip=True)
        team = re.sub(r'^\d+', '', raw_team).strip()

        points_text = cols[-2].get_text(strip=True)
        try:
            points = int(points_text)
        except ValueError:
            print(f"Skipping team '{team}' due to invalid points value: '{points_text}'")
            continue

        table.append({"Position": i, "Team": team, "Points": points})
    return pd.DataFrame(table)


def score_prediction(pred_row, real_df, league):
    """
    Comparison between prediction and real table, this should be correct as it stands,
    but if not there will be a systematic error in the calculation.
    """
    team = pred_row["Team"]
    pred_pos = int(pred_row["Position"])

    real_row = real_df[real_df["Team"].str.lower() == team.lower()]
    if real_row.empty:
        return None

    position_to_points = dict(zip(real_df['Position'], real_df['Points']))
    real_pos = int(real_row["Position"].iloc[0])
    real_pts = int(real_row["Points"].iloc[0])
    # actual_points = int(real_row['Points'])
    target_points = position_to_points.get(pred_pos, None)

    score = 0
    if real_pos == pred_pos:
        score += 9
    elif abs(real_pts - target_points) <=3:
        score += 2
    if abs(real_pos - pred_pos) == 1:
        score += 1

    if get_zone(real_pos, league) == get_zone(pred_pos, league):
        score += 1

    return {
        "Team": team,
        "Predicted": pred_pos,
        "Real": real_pos,
        "Points_Diff": abs(real_pts - target_points),
        "Score": score,
    }

def generate_html(real_tables, user_results, user_totals):
    """
    Where the main section happens, This generates the HTML and will only work
    if all of the functions before this have run successfully.
    ONLY Edit the HTML here to ensure the next version has the same changes.
    DO NOT edit the final_results.html file - IT WILL NOT BE THERE NEXT TIME!!! 
    """
    # Build HTML as a string - change this so it creates a readable HTML.
    html = """
    <html><head><title>Predictor League Final Results</title>
    <style>
    body { 
      font-family: Arial, sans-serif; 
      background: #460001;
      padding: 20px;
      color: white;
    }
    table { 
      border-collapse: collapse;
      width: 100%; 
      background: rgb(8, 2, 35);
      margin-bottom: 2em; 
    }
    th, td { 
      border: 1px solid #ccc; 
      padding: 5px 10px; 
      text-align: center;
    }
    th { 
      background-color: #034f27; 
    }
    .score { 
      font-weight: bold; 
    }
    .team-cell {
      display: flex;
      align-items: center;
      gap: 6px;
      justify-content: flex-start;
    }
    .team-logo {
      width: 20px;
      height: 20px;
      object-fit: contain;
    }
    </style>
    <script src="../TeamData.js"></script>
    </head><body>
    <h1>Predictor League - Final Results</h1>
    <p>Tables are pulled directly from the BBC Sports website</p>
    """

    # Leaderboard
    html += "<h2>Leaderboard</h2><table><thead><tr><th>Player</th><th>Premier League</th><th>Championship</th><th>Total</th></tr></thead><tbody>"
    leaderboard = sorted(user_totals.items(), key=lambda x: x[1]['Total'], reverse=True)
    for name, scores in leaderboard:
        html += f"<tr><td>{name}</td><td>{scores['Premier League']}</td><td>{scores['Championship']}</td><td><strong>{scores['Total']}</strong></td></tr>"
    html += "</tbody></table>\n"

    # Actual tables
    for league, df in real_tables.items():
        html += f"<h2>{league} - Actual Table</h2>\n"
        html += "<table><thead><tr><th>Position</th><th>Team</th><th>Points</th></tr></thead><tbody>\n"
        for _, row in df.iterrows():
            html += f"<tr><td>{row['Position']}</td><td class='team-name' data-team='{row['Team']}'>{row['Team']}</td><td>{row['Points']}</td></tr>\n"
        html += "</tbody></table>\n"

    # Predictions
    for player, leagues in user_results.items():
        total_score = user_totals[player]['Total']
        html += f"<h2>Predictions & Scores for {player} (Total: {total_score})</h2>\n"
        for league, scores in leagues.items():
            running_total = 0
            league_score = user_totals[player][league]
            html += f"<h3>{league} (Score: {league_score})</h3>\n"
            html += "<table><thead><tr><th>Predicted</th><th>Team</th><th>Actual</th><th>Points Diff</th><th>Score</th><th>Running Total</th></tr></thead><tbody>\n"
            for s in scores:
                running_total += s['Score']
                html += f"<tr><td>{s['Predicted']}</td><td class='team-name' data-team='{s['Team']}'>{s['Team']}</td><td>{s['Real']}</td><td>{s['Points_Diff']}</td><td class='score'>{s['Score']}</td><td>{running_total}</td></tr>\n"
            html += "</tbody></table>\n"

    # JS to style team cells
    html += """
    <script>
    document.querySelectorAll(".team-name").forEach(cell => {
    const team = cell.dataset.team;
    if (teamColours[team]) {
        cell.style.backgroundColor = teamColours[team].bg;
        cell.style.color = teamColours[team].fg;
    }
    if (teamLogos[team]) {
        const logo = document.createElement("img");
        logo.src = teamLogos[team];
        logo.className = "team-logo";
        const wrapper = document.createElement("div");
        wrapper.className = "team-cell";
        wrapper.appendChild(logo);
        wrapper.appendChild(document.createTextNode(team));
        cell.innerHTML = "";
        cell.appendChild(wrapper);
    }
    });
    </script>
    </body></html>
    """

    return html

def main(): 
    """
    Does the stuff, runs everything but issues will likely be in other definitions.
    """
    # Read predictions CSV - must have columns: Name, League, Position, Team
    predictions = pd.read_csv("Predictions/predictions.csv")

    real_tables = {}
    for league in predictions["League"].unique():
        real_tables[league] = scrape_table(league)

    user_results = {}
    user_totals = {}

    for name in predictions["Name"].unique():
        user_results[name] = {}
        user_totals[name] = {"Premier League": 0, "Championship": 0, "Total": 0}
        user_preds = predictions[predictions["Name"] == name]
        for league in user_preds["League"].unique():
            league_preds = user_preds[user_preds["League"] == league]
            scored_list = []
            for _, row in league_preds.iterrows():
                score = score_prediction(row, real_tables[league], league)
                if score:
                    scored_list.append(score)
                    user_totals[name][league] += score["Score"]
                    user_totals[name]["Total"] += score["Score"]
            user_results[name][league] = scored_list

    html_content = generate_html(real_tables, user_results, user_totals)

    with open("Predictions/final_results.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("final_results.html generated!")


if __name__ == "__main__":
    main()
