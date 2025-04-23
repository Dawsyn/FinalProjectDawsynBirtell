import requests
import sqlite3 
from datetime import datetime


date_str = datetime.now().strftime("%Y%m%d")

url = "https://nba-api-free-data.p.rapidapi.com/nba-scoreboard-by-date"

querystring = {"date":date_str}

headers = {
"x-rapidapi-key": "e1cac09505msh874e3ef17649cc2p14a0d9jsn181a6a590be6",
"x-rapidapi-host": "nba-api-free-data.p.rapidapi.com"
}


def save_scores_to_db(data):
    

	
    conn = sqlite3.connect("instance/flaskr.sqlite")
    cur = conn.cursor()
    

    for event in data['response']['Events']:
        game_id = event['id']
        game_date = event['date']
        comps = event['competitions']['competitors']

        home = next(c for c in comps if c['homeAway'] == 'home')
        away = next(c for c in comps if c['homeAway'] == 'away')
        
        clean_date = game_date.replace('Z', '')  # Remove 'Z' if exists
        formatted_date = datetime.fromisoformat(clean_date).strftime("%m/%d/%Y")

        cur.execute("""
            INSERT OR IGNORE INTO scoreboard (game_id, game_date, home_team, home_score, away_team, away_score, game_status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            game_id,
            formatted_date,
            home['team']['displayName'],
            int(home['score']),
            away['team']['displayName'],
            int(away['score']),
            event['status']['type']['shortDetail']
        ))

    conn.commit()
    conn.close()

# Fetch from API
response = requests.get(url, headers=headers, params=querystring)
data = response.json()
save_scores_to_db(data)