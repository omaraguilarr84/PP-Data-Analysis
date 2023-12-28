import pandas as pd  # type: ignore
from bs4 import BeautifulSoup
import requests
from unidecode import unidecode

# function that returns a player's game log in a given season
# player: player's full name (e.g. Stephen Curry)
def get_player_game_log(player: str, season: int) -> pd.DataFrame:
    """A function to retrieve a player's game log in a given season.

    Returns a pandas DataFrame of a NBA player's game log in a given season, including position-specific statistics.

    Args:
        player (str): A NBA player's full name, as it appears on Basketball Reference
        season (int): The season of the game log you are trying to retrieve

    Returns:
        pandas.DataFrame: Each game is a row of the DataFrame

    """

    # make request to find proper href
    r1 = make_request_list(player, season)
    player_list = get_soup(r1)

    # find href
    href = get_href(player, season, player_list)

    # make HTTP request and extract HTML
    r2 = make_request_player(href, season)

    # parse HTML using BeautifulSoup
    game_log = get_soup(r2)

    return p_game_log(game_log)

# helper function that gets the player's href
def get_href(player: str, season: int, player_list: BeautifulSoup) -> str:
    players_table = player_list.find('table', id = 'players')
    players_rows = players_table.find('tbody').find_all('tr')
    for p in players_rows:
        year_min = p.find('td', {'data-stat': 'year_min'}).text
        year_max = p.find('td', {'data-stat': 'year_max'}).text
        seasons = [year_min, year_max]
        players = p.find('th', {'data-stat': 'player'}).text
        players = unidecode(players)
        if season >= int(seasons[0]) and season <= int(seasons[1]) and player in players:
            return p.find('a').get('href').replace('.html', '')
    raise Exception(f'Cannot find {player} from {str(season)}')


# helper function that makes a HTTP request over a list of players with a given last initial
def make_request_list(player: str, season: int):
    name_split = player.split(' ')
    last_initial = name_split[1][0].lower()
    url = 'https://www.basketball-reference.com/players/%s/' % (last_initial)
    return requests.get(url)


# helper function that makes a HTTP request for a given player's game log
def make_request_player(href: str, season: int):
    url = 'https://www.basketball-reference.com%s/gamelog/%s/' % (href, season)
    return requests.get(url)


# helper function that takes a requests.Response object and returns a BeautifulSoup object
def get_soup(request):
    return BeautifulSoup(request.text, 'html.parser')


# helper function that takes a BeautifulSoup object and converts it into a pandas dataframe containing a QB game log
def p_game_log(soup: BeautifulSoup) -> pd.DataFrame:
    # Most relevant QB stats, in my opinion. Could adjust if necessary
    data = {
        'game': [],
        'date': [],
        'team': [],
        'game_location': [],
        'opp': [],
        'result': [],
        'fg': [],
        'fga': [],
        'fg3': [],
        'fg3a': [],
        'ft': [],
        'fta': [],
        'orb': [],
        'drb': [],
        'reb': [],
        'ast': [],
        'stl': [],
        'blk': [],
        'tov': [],
        'pf': [],
        'pts': [],
    }  # type: dict

    # find table rows excluding those with class 'thead'
    table_rows = soup.find('tbody').find_all('tr', class_=lambda x: x != 'thead')

    # ignore inactive or DNP games
    to_ignore = []
    for i in range(len(table_rows)):
        elements = table_rows[i].find_all('td')
        x = elements[len(elements) - 1].text
        if x == 'Inactive' or x == 'Did Not Play' or x == 'Injured Reserve' or x == 'Did Not Dress' or x == 'Not With Team':
            to_ignore.append(i)

    # adding data to data dictionary
    for i in range(len(table_rows)):
        if i not in to_ignore:
            # Need to fix logic within these to match data dict
            data['game'].append(int(table_rows[i].find('td', {'data-stat': 'game_season'}).text))
            data['date'].append(table_rows[i].find('td', {'data-stat': 'date_game'}).text)
            data['team'].append(table_rows[i].find('td', {'data-stat': 'team_id'}).text)
            data['game_location'].append(table_rows[i].find('td', {'data-stat': 'game_location'}).text)
            data['opp'].append(table_rows[i].find('td', {'data-stat': 'opp_id'}).text)
            data['result'].append(table_rows[i].find('td', {'data-stat': 'game_result'}).text.split(' ')[0])
            data['fg'].append(int(table_rows[i].find('td', {'data-stat': 'fg'}).text)) if table_rows[i].find('td', {'data-stat': 'fg'}).text != '' else data['fg'].append(0)
            data['fga'].append(int(table_rows[i].find('td', {'data-stat': 'fga'}).text)) if table_rows[i].find('td', {'data-stat': 'fga'}).text != '' else data['fga'].append(0)
            data['fg3'].append(int(table_rows[i].find('td', {'data-stat': 'fg3'}).text)) if table_rows[i].find('td', {'data-stat': 'fg3'}).text != '' else data['fg3'].append(0)
            data['fg3a'].append(int(table_rows[i].find('td', {'data-stat': 'fg3a'}).text)) if table_rows[i].find('td', {'data-stat': 'fg3a'}).text != '' else data['fg3a'].append(0)
            data['ft'].append(int(table_rows[i].find('td', {'data-stat': 'ft'}).text)) if table_rows[i].find('td', {'data-stat': 'ft'}).text != '' else data['ft'].append(0)
            data['fta'].append(int(table_rows[i].find('td', {'data-stat': 'fta'}).text)) if table_rows[i].find('td', {'data-stat': 'fta'}).text != '' else data['fta'].append(0)
            data['orb'].append(int(table_rows[i].find('td', {'data-stat': 'orb'}).text)) if table_rows[i].find('td', {'data-stat': 'orb'}).text != '' else data['orb'].append(0)
            data['drb'].append(int(table_rows[i].find('td', {'data-stat': 'drb'}).text)) if table_rows[i].find('td', {'data-stat': 'drb'}).text != '' else data['drb'].append(0)
            data['reb'].append(int(table_rows[i].find('td', {'data-stat': 'trb'}).text)) if table_rows[i].find('td', {'data-stat': 'trb'}).text != '' else data['trb'].append(0)
            data['ast'].append(int(table_rows[i].find('td', {'data-stat': 'ast'}).text)) if table_rows[i].find('td', {'data-stat': 'ast'}).text != '' else data['ast'].append(0)
            data['stl'].append(int(table_rows[i].find('td', {'data-stat': 'stl'}).text)) if table_rows[i].find('td', {'data-stat': 'stl'}).text != '' else data['stl'].append(0)
            data['blk'].append(int(table_rows[i].find('td', {'data-stat': 'blk'}).text)) if table_rows[i].find('td', {'data-stat': 'blk'}).text != '' else data['blk'].append(0)
            data['tov'].append(int(table_rows[i].find('td', {'data-stat': 'tov'}).text)) if table_rows[i].find('td', {'data-stat': 'tov'}).text != '' else data['tov'].append(0)
            data['pf'].append(int(table_rows[i].find('td', {'data-stat': 'pf'}).text)) if table_rows[i].find('td', {'data-stat': 'pf'}).text != '' else data['pf'].append(0)
            data['pts'].append(int(table_rows[i].find('td', {'data-stat': 'pts'}).text)) if table_rows[i].find('td', {'data-stat': 'pts'}).text != '' else data['pts'].append(0)

    return pd.DataFrame(data=data)

def main():
    print(get_player_game_log('Zion Williamson', 2024))


if __name__ == '__main__':
    main()