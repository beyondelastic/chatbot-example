import os
import datetime
import requests
from gptrim import trim
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BING_SEARCH_API_KEY = os.getenv('BING_KEY')
BING_SEARCH_ENDPOINT = os.getenv('BING_URL')

EUROCUP_URL = "https://www.euroleaguebasketball.net/en/eurocup/game-center/"

def search_internet(query):
    """
    Use Bing Search API to provide context
    """
    endpoint = f"{BING_SEARCH_ENDPOINT}"
    params = {
        'q': f"site:euroleaguebasketball.net {query}",  # Add site filter to query
        'count': 5,
        'responseFilter': 'webpages',
        'freshness': 'month'
    }
    current_date = datetime.date.today()
    past_month_start = current_date - datetime.timedelta(days=30)
    params['freshnessstartdate'] = past_month_start.strftime('%Y-%m-%d')
    params['freshnessenddate'] = current_date.strftime('%Y-%m-%d')
    headers = { 'Ocp-Apim-Subscription-Key': BING_SEARCH_API_KEY }
    # Call the API
    response = requests.get(endpoint, headers=headers, params=params)
    
    if response.status_code == 200:
        response_json = response.json()
        search_results = response_json.get('webPages', {}).get('value', [])
        result_text = ''
        for result in search_results:
            title = result.get('name', '')
            snippet = result.get('snippet', '')
            url = result.get('url', '')
            result_text += f'Title: {title}\nSnippet: {snippet}\nURL: {url}\n\n'

        search_prompt = f"""
        Based on the internet search results provided in <>, provide an answer to the query [] if it is relevant along with a source URL. \
        If there are no internet search results or if they are not relevant then say \"Please try again.\"\
        
        context:<{trim(result_text)}>
        query:[{query}]
        """

        print('Original text source:\n' + result_text)

        print('Trimmed text source:\n' + trim(result_text))

        return {"role": "system", "content": search_prompt}
    
    else:
        return {"role": "system", "content": "Say: 'Please try again.'"}