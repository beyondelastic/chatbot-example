import os
import datetime
import requests
from bs4 import BeautifulSoup
from gptrim import trim
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

EUROCUP_URL = "https://www.euroleaguebasketball.net/en/eurocup/game-center/"

def fetch_latest_game_results():
    response = requests.get(EUROCUP_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        games = soup.find_all('div', class_='game-result')
        results = []
        for game in games:
            teams = game.find_all('div', class_='team-name')
            scores = game.find_all('div', class_='team-score')
            if teams and scores:
                team1 = teams[0].text.strip()
                team2 = teams[1].text.strip()
                score1 = scores[0].text.strip()
                score2 = scores[1].text.strip()
                results.append(f"{team1} {score1} - {team2} {score2}")
        return "\n".join(results)
    else:
        return "Could not fetch the latest game results."
    


