import pandas as pd  # type: ignore
from bs4 import BeautifulSoup
import requests

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
    players = player_list.find('div', id='div_players').find_all('p')
    for p in players:
        seasons = p.text.split(' ')
        seasons = seasons[len(seasons) - 1].split('-')
        if season >= int(seasons[0]) and season <= int(seasons[1]) and player in p.text:
            return p.find('a').get('href').replace('.htm', '')
    raise Exception('Cannot find ' + player + ' from ' + str(season))


# helper function that makes a HTTP request over a list of players with a given last initial
def make_request_list(player: str, season: int):
    name_split = player.split(' ')
    last_initial = name_split[1][0]
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
        'game_season': [],
        'date_game': [],
        'team_id': [],
        'game_location': [],
        'opp_id': [],
        'result': [],
        'fg': [],
        'fga': [],
        'fg3': [],
        'fg3a': [],
        'ft': [],
        'fta': [],
        'orb': [],
        'drb': [],
        'ast': [],
        'stl': [],
        'blk': [],
        'tov': [],
        'pf': [],
        'pts': [],
    }  # type: dict

    table_rows = soup.find('tbody').find_all('tr')

    # ignore inactive or DNP games
    to_ignore = []
    for i in range(len(table_rows)):
        elements = table_rows[i].find_all('td')
        x = elements[len(elements) - 1].text
        if x == 'Inactive' or x == 'Did Not Play' or x == 'Injured Reserve' or x == 'Did Not Dress':
            to_ignore.append(i)

    # adding data to data dictionary
    for i in range(len(table_rows)):
        if i not in to_ignore:
            # Need to fix logic within these to match data dict
            data['date'].append(table_rows[i].find('td', {'data-stat': 'game_date'}).text)
            data['week'].append(int(table_rows[i].find('td', {'data-stat': 'week_num'}).text))
            data['team'].append(table_rows[i].find('td', {'data-stat': 'team'}).text)
            data['game_location'].append(table_rows[i].find('td', {'data-stat': 'game_location'}).text)
            data['opp'].append(table_rows[i].find('td', {'data-stat': 'opp'}).text)
            # Need to fix logic for game_result
            data['result'].append(table_rows[i].find('td', {'data-stat': 'game_result'}).text.split(' ')[0])

    return pd.DataFrame(data=data)

def main():
    print(get_player_game_log('Stephen Curry', 2021))


if __name__ == '__main__':
    main()