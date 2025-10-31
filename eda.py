import pandas as pd
import os

# Directory containing the CSV files
data_dir = 'data/'

# List all CSV files in the directory (excluding the merged file if it exists)
csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv') and f != 'boss_merge.csv']

# Initialize an empty list to hold DataFrames
dfs = []

# Read each CSV file and append to the list
for file in csv_files:
    file_path = os.path.join(data_dir, file)
    df = pd.read_csv(file_path, encoding='latin1')
    dfs.append(df)

# Concatenate all DataFrames
if dfs:
    merged_df = pd.concat(dfs, ignore_index=True)
    
    # Save the merged DataFrame to a new CSV file
    output_path = os.path.join(data_dir, 'boss_merge.csv')
    merged_df.to_csv(output_path, index=False)
    print(f"Merged {len(csv_files)} CSV files into {output_path}")
else:
    print("No CSV files found to merge.")

# print stuff
df = pd.read_csv("data/boss_merge.csv")
print(df["School/Department"].value_counts())

df_is_only = df[df["School/Department"] == "SIS"].copy()

df_is_only.to_csv("data/sis_only.csv", index=False)
