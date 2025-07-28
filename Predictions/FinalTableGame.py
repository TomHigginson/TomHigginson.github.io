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
    for i, (start, end) in enumerate(ZONES[league]):
        if start <= pos <= end:
            return i
    return -1

def scrape_table(league):
    url = BBC_URLS[league]
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    rows = soup.select("table tbody tr")

    table = []
    for i, row in enumerate(rows, start=1):
        cols = row.find_all("td")
        if len(cols) < 10:
            # Might be a summary row or something else; skip
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
    team = pred_row["Team"]
    pred_pos = int(pred_row["Position"])

    real_row = real_df[real_df["Team"].str.lower() == team.lower()]
    if real_row.empty:
        return None

    position_to_points = dict(zip(real_df['Position'], real_df['Points']))
    real_pos = int(real_row["Position"].iloc[0])
    real_pts = int(real_row["Points"].iloc[0])
    actual_points = int(real_row['Points'])
    target_points = position_to_points.get(pred_pos, None)

    score = 0
    if real_pos == pred_pos:
        score += 9
    elif abs(actual_points - target_points) <=3:
        score += 2
    if abs(real_pos - pred_pos) == 1:
        score += 1

    if get_zone(real_pos, league) == get_zone(pred_pos, league):
        score += 1

    return {
        "Team": team,
        "Predicted": pred_pos,
        "Real": real_pos,
        "Points": real_pts,
        "Score": score,
    }

def generate_html(real_tables, user_results):
    # Build HTML as a string
    html = """
    <html><head><title>Predictor League Final Results</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 20px; }
      table { border-collapse: collapse; width: 100%; margin-bottom: 2em; }
      th, td { border: 1px solid #ccc; padding: 5px 10px; }
      th { background: #eee; }
      .score { text-align: center; font-weight: bold; }
      h2 { margin-top: 40px; }
    </style>
    </head><body>
    <h1>Predictor League - Final Results</h1>
    Tables are pulled directly from the bbc sports website
    """

    for league, df in real_tables.items():
        html += f"<h2>{league} - Actual Table</h2>"
        html += "<table><thead><tr>""<th>Position</th>""<th>Team</th>""<th>Points</th>""</tr></thead><tbody>" 
        for _, row in df.iterrows():
            html += f"<tr><td>{row['Position']}</td><td>{row['Team']}</td><td>{row['Points']}</td></tr>"
        html += "</tbody></table>"

    for player, leagues in user_results.items():
        html += f"<h2>Predictions & Scores for {player}</h2>"
        for league, scores in leagues.items():
            html += f"<h3>{league}</h3>"
            html += "<table><thead><tr><th>Predicted</th><th>Team</th><th>Actual</th><th>Points</th><th>Score</th></tr></thead><tbody>"
            for s in scores:
                html += f"<tr><td>{s['Predicted']}</td><td>{s['Team']}</td><td>{s['Real']}</td><td>{s['Points']}</td><td class='score'>{s['Score']}</td></tr>"
            html += "</tbody></table>"
    html += "</body></html>"
    return html

def main():
    # Read predictions CSV - must have columns: Name, League, Position, Team
    predictions = pd.read_csv("Predictions/predictions.csv")

    real_tables = {}
    for league in predictions["League"].unique():
        real_tables[league] = scrape_table(league)

    user_results = {}
    for name in predictions["Name"].unique():
        user_results[name] = {}
        user_preds = predictions[predictions["Name"] == name]
        for league in user_preds["League"].unique():
            league_preds = user_preds[user_preds["League"] == league]
            scored_list = []
            for _, row in league_preds.iterrows():
                score = score_prediction(row, real_tables[league], league)
                if score:
                    scored_list.append(score)
            user_results[name][league] = scored_list

    html_content = generate_html(real_tables, user_results)

    with open("final_results.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("final_results.html generated!")

if __name__ == "__main__":
    main()
