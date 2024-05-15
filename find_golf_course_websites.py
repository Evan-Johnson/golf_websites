import pandas as pd
from googlesearch import search
import time

input_file = 'golf2.csv'
output_file = 'updated_golf_courses.csv'

df = pd.read_csv(input_file)
if 'Website' not in df.columns:
    df['Website'] = None

def find_website(name):
    try:
        for j in search(name + ' golf course', num_results=1, sleep_interval=5):
            return j
    except Exception as e:  # Catch any exception during the search
        print(f"Error occurred while searching for {name}: {e}")
        return None  # Return None if there's an error
    return None

for i, row in df.iterrows():
    if pd.isna(row['Website']):
        print(f"Finding website for {row['Golf Course Name']}...")
        df.at[i, 'Website'] = find_website(row['Golf Course Name'])
        time.sleep(45)  # Increase delay to 60 seconds

df.to_csv(output_file, index=False)
print('Updated spreadsheet saved to', output_file)
