from pro_football_reference_web_scraper import player_game_log as p

def get_pdata(player, position, year):
    game_log = p.get_player_game_log(player, position, season = 2023)
    return game_log

def over(game_log, threshold, column_name):
    total_games = len(game_log)
    games_over_threshold = len(game_log[game_log[column_name] > threshold])
    percentage_over_threshold = (games_over_threshold / total_games) * 100
    return percentage_over_threshold

player = 'Lamar Jackson'
position = 'QB'
year = 2023
threshold = 199.5
stat = 'pass_yds'

game_log = get_pdata(player, position, year)
per_over = over(game_log, threshold, stat)
print(per_over)