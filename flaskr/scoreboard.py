import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from balldontlie import BalldontlieAPI



# Load .env and initialize API
load_dotenv()
api = BalldontlieAPI(api_key=os.getenv("API_KEY"))

# Connect to SQLite DB
conn = sqlite3.connect("instance/flaskr.sqlite")
cur = conn.cursor()

# Ensure the scoreboard table exists
cur.execute("""
CREATE TABLE IF NOT EXISTS scoreboard (
    game_id INTEGER PRIMARY KEY,
    game_date TEXT,
    home_team TEXT,
    home_score INTEGER,
    away_team TEXT,
    away_score INTEGER,
    period_number INTEGER,
    game_status TEXT
)
""")

# Fetch and store games
cursor = None
total = 0

while True:
    print(f"🔄 Fetching games with cursor: {cursor or 'start'}")

    params = {
        "seasons": [2024],
        "per_page": 100
    }
    if cursor:
        params["cursor"] = cursor

    games_data = api.nba.games.list(**params)
    data = games_data.data
    meta = games_data.meta

    for game in data:
        try:
            formatted_date = datetime.strptime(game.date[:10], "%Y-%m-%d").strftime("%m/%d/%Y")
            
            cur.execute("""
                INSERT OR IGNORE INTO scoreboard (
                    game_id, game_date, home_team, home_score,
                    away_team, away_score, period_number, game_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                game.id,
                formatted_date,
                game.home_team.full_name,
                game.home_team_score,
                game.visitor_team.full_name,
                game.visitor_team_score,
                game.period,
                game.status
            ))
            total += 1
        except Exception as e:
            print(f"❌ Failed to insert game {game.id}: {e}")

    cursor = meta.next_cursor
    if not cursor:
        break

# Finalize
conn.commit()
conn.close()
print(f"✅ Done! Total games inserted: {total}")
