import pandas as pd

output_file_path = '/Users/omaraguilarjr/PP-Data-Analysis/Data/pfrData.csv'
output_data = pd.read_csv(output_file_path)

top_n = 6

sorted_data = output_data.sort_values(by='Percentage', ascending=False)

top_n_percentages = sorted_data.head(top_n)

print(f"Top {top_n} Percentages:")
print(top_n_percentages[['Player', 'Stat', 'Threshold', 'Percentage']])