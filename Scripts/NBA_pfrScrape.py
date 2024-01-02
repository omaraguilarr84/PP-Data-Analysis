from sports_reference_scrapers import nba_player_game_log as p
import pandas as pd
import time
import numpy as np

def get_pdata(player, year):
    try:
        game_log = p.get_player_game_log(player, season=year)
        return game_log
    except Exception as e:
        print(f"Error fetching game log for {player}: {e}")
        time.sleep(time_limit_seconds/requests_per_minute_limit)
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

def vs_opp(game_log, opp, stat):
    games_vs_opp = game_log[game_log['opp'] == opp]

    if games_vs_opp.empty:
        return None

    avg_vs_opp = np.mean(games_vs_opp[stat])
    return avg_vs_opp

def dyn_stat(new_stat, stat1, stat2, func):
    if func == 'add':
        if stat1 in game_log.columns and stat2 in game_log.columns:
            game_log[new_stat] = game_log[stat1] + game_log[stat2]
        elif stat1 in game_log.columns:
            game_log[new_stat] = game_log[stat1]
        elif stat2 in game_log.columns:
            game_log[new_stat] = game_log[stat2]

    if func == 'percentage':
        game_log[new_stat] = (game_log[stat1] / game_log[stat2]) * 100

def dyn_stat3(new_stat, stat1, stat2, stat3, func):
    if func == 'add':
        game_log[new_stat] = game_log[stat1] + game_log[stat2] + game_log[stat3]

requests_per_minute_limit = 15
time_limit_seconds = 60

input_file_path = '/Users/omaraguilarjr/PP-Data-Analysis/Data/NBA_ppData.csv'
input_data = pd.read_csv(input_file_path, skiprows=0)

stat_mapping = {
    'Pts+Rebs+Asts': 'pts_reb_ast',
    'Points': 'pts',
    'Rebounds': 'reb',
    'Assists': 'ast',
    'Defensive Rebounds': 'drb',
    'Offensive Rebounds': 'orb',
    '3-PT Attempted': 'fg3a',
    'Free Throws Made': 'ft',
    'FG Attempted': 'fga',
    'Pts+Rebs': 'pts_reb',
    'Pts+Asts': 'pts_ast',
    '3-PT Made': 'fg3',
    'Blocked Shots': 'blk',
    'Steals': 'stl',
    'Rebs+Asts': 'reb_ast',
    'Blks+Stls': 'blk_stl',
    'Turnovers': 'tov'
}

output_data_list = []

for index, row in input_data.iterrows():
    player = str(row.iloc[0])
    opp = str(row.iloc[2])
    threshold = row.iloc[3]
    input_stat = str(row.iloc[4])
    stat = stat_mapping.get(input_stat)

    print(f"Fetching data for {player}, Year 2024...")
    
    if stat is None:
        print(f"Error: Input stat '{input_stat}' not found in stat mapping. Skipping.")
        continue
    
    game_log = get_pdata(player, 2024)
    
    if game_log is None:
        print(f"Error fetching game log for {player}. Skipping.")
        continue

    print(f"Input Stat: {input_stat}, Mapped Stat: {stat}")
    
    if stat == 'pts_reb_ast':
        dyn_stat3(stat, 'pts', 'reb', 'ast','add')
    elif stat == 'pts_reb':
        dyn_stat(stat, 'pts', 'reb', 'add')
    elif stat == 'pts_ast':
        dyn_stat(stat, 'pts', 'ast', 'add')
    elif stat == 'reb_ast':
        dyn_stat(stat, 'reb', 'ast', 'add')
    elif stat == 'blk_stl':
        dyn_stat(stat, 'blk', 'stl', 'add')
    
    per_over = over(game_log, threshold, stat)
    avg = np.mean(game_log[stat])
    avg_vs_opp = vs_opp(game_log, opp, stat)
    output_data = output_data_list.append({'Player': player, 'Stat': input_stat, 'Threshold': threshold, 'Percentage': per_over, 'Average': avg, 'Avg vs. Opp': avg_vs_opp})

    print(f'{index + 1}/{len(input_data)}')
    time.sleep(time_limit_seconds / requests_per_minute_limit)

output_data = pd.DataFrame(output_data_list)

output_file_name = 'NBA_pfrData.csv'
output_file_path = '/Users/omaraguilarjr/PP-Data-Analysis/Data'
output_full_path = f'{output_file_path}/{output_file_name}'
output_data.to_csv(output_full_path, index=False)