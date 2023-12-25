from pro_football_reference_web_scraper import player_game_log as p
import pandas as pd
import time

def get_pdata(player, position, year):
    try:
        game_log = p.get_player_game_log(player, position, season=year)
        return game_log
    except Exception as e:
        print(f"Error fetching game log for {player}: {e}")
        return None

def over(game_log, threshold, column_name):
    if game_log is None or column_name is None:
        print("Error: Game log or column name is None.")
        return None

    if column_name not in game_log.columns:
        print(f"Error: Column '{column_name}' not found in game log.")
        return None

    games_over_threshold = len(game_log[game_log[column_name] > threshold])
    total_games = len(game_log)
    percentage_over_threshold = (games_over_threshold / total_games) * 100
    return percentage_over_threshold

def dyn_stat(new_stat, stat1, stat2, func):
    if func == 'add':
        game_log[new_stat] = game_log[stat1] + game_log[stat2]
        return game_log[new_stat]

    if func == 'percentage':
        game_log[new_stat] = (game_log[stat1] / game_log[stat2]) * 100
        return game_log[new_stat]

requests_per_minute_limit = 19
time_limit_seconds = 60

input_file_path = '/Users/omaraguilarjr/PP-Data-Analysis/Data/122223.csv'
input_data = pd.read_csv(input_file_path, skiprows=0)

stat_mapping = {
    'Pass Yards': 'pass_yds',
    'Receiving Yards': 'rec_yds',
    'Rush Yards': 'rush_yds',
    'Pass TDs': 'pass_td',
    'Receptions': 'rec',
    'Rush+Rec TDs': 'rush_rec_td',
    'Pass Attempts': 'att',
    'Pass Completions': 'cmp',
    'INT': 'int',
    'Pass+Rush Yds': 'pass_rush_yds',
    'Rush Attempts': 'rush_att',
    'Rec Targets': 'tgt',
    'Completion Percentage': 'cmp_per'
}

output_data_list = []

for index, row in input_data.iloc[:5].iterrows():
    player = str(row.iloc[0])
    position = str(row.iloc[1])
    threshold = row.iloc[3]
    input_stat = str(row.iloc[4])
    stat = stat_mapping.get(input_stat)

    print(f"Fetching data for {player} ({position}), Year 2023...")
    
    if stat is None:
        print(f"Error: Input stat '{input_stat}' not found in stat mapping. Skipping.")
        continue
    
    game_log = get_pdata(player, position, 2023)
    
    if game_log is None:
        print(f"Error fetching game log for {player}. Skipping.")
        continue
    
    print(f"Input Stat: {input_stat}, Mapped Stat: {stat}")
    
    if stat == 'rush_rec_td':
        game_log['rush_rec_td'] = game_log['rush_td'] + game_log['rec_td']
    
    if stat == 'pass_rush_yds':
        game_log['pass_rush_yds'] = game_log['pass_yds'] + game_log['rush_yds']

    if stat == 'cmp_per':
        game_log['cmp_per'] = (game_log['cmp'] / game_log['att']) * 100
    
    per_over = over(game_log, threshold, stat)
    output_data = output_data_list.append({'Player': player, 'Stat': stat, 'Percentage': per_over})

    time.sleep(time_limit_seconds / requests_per_minute_limit)

output_data = pd.DataFrame(output_data_list)

output_file_name = '122223_output.csv'
output_file_path = '/Users/omaraguilarjr/PP-Data-Analysis/Data'
output_full_path = f'{output_file_path}/{output_file_name}'
output_data.to_csv(output_full_path, index=False)