import pandas as pd

league = input("What league? ")

pfrData_file_path = f'/Users/omaraguilarjr/PP-Data-Analysis/Data/{league}_pfrData.csv'
pfrData = pd.read_csv(pfrData_file_path)

valid_resp = ['high', 'low', 'both']

def high(num):
   sorted_data = pfrData.sort_values(by = 'Percentage', ascending = False)
   top_n_percentages = sorted_data.head(num)
   return top_n_percentages

def low(num):
    sorted_data = pfrData.sort_values(by = 'Percentage', ascending = True)
    bot_n_percentages = sorted_data.head(num)
    return bot_n_percentages

def both(num):
    sorted_data_100 = pfrData.assign(abs_diff=lambda x: abs(x['Percentage'] - 100)).sort_values(by = 'abs_diff', ascending = True)
    sorted_data_0 = pfrData.assign(abs_diff=lambda x: abs(x['Percentage'])).sort_values(by = 'abs_diff', ascending = True)
    sorted_data = pd.concat([sorted_data_100, sorted_data_0]).sort_values(by = 'abs_diff', ascending = True)
    combined_data = sorted_data.head(num)
    return combined_data

num = int(input("How many picks? "))
if num > len(pfrData):
    print(f"Warning: Only {len(pfrData)} data points available.")
    num = len(pfrData)

resp = input("High, low, or both percentages? (high, low, or both) ")
while resp not in valid_resp:
    print("Invalid response. Please enter 'high', 'low', or 'both'.")
    resp = input("High, low, or both percentages? (high, low, or both) ")

if resp == 'high':
    top_n_percentages = high(num)
    print(f"Top {num} Percentages:")
    print(top_n_percentages[['Player', 'Stat', 'Threshold', 'Percentage']])
elif resp == 'low':
    bot_n_percentages = low(num)
    print(f"Bottom {num} Percentages:")
    print(bot_n_percentages[['Player', 'Stat', 'Threshold', 'Percentage']])
elif resp == 'both':
    combined_percentages = both(num)
    print(f"Top {num} Combined Percentages:")
    print(combined_percentages[['Player', 'Stat', 'Threshold', 'Percentage']])