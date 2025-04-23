import sqlite3
from flask import Blueprint, render_template, request
from datetime import datetime
from dotenv import load_dotenv
from balldontlie import BalldontlieAPI
import os

load_dotenv()
api = BalldontlieAPI(api_key=os.getenv("API_KEY"))
cursor = None
total = 0

while True:
    print(f"🔄 Fetching games with cursor: {cursor or 'start'}")
    
    # Prepare query
    params = {
        "seasons": [2024],
        "per_page": 100
    }
    if cursor:
        params["cursor"] = cursor

    # API call
    games_data = api.nba.games.list(**params)
    data = games_data.data
    meta = games_data.meta


    # Print each game
    for game in data:
        total += 1
        date = game.date[:10]
        home = game.home_team.full_name
        away = game.visitor_team.full_name
        score = f"{game.visitor_team_score} - {game.home_team_score}"
        status = game.status
        print(f"{total}. {date}: {away} @ {home} — {score} [{status}]")

    # Move to next page if there is one
    cursor = meta.next_cursor    
    if not cursor:
        print(f"✅ Done! Total games printed: {total}")
        break