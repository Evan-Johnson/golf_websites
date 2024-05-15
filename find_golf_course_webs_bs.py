import pandas as pd
import time
import requests
from bs4 import BeautifulSoup

input_file = 'golf3.csv'
output_file = 'updated_golf_courses.csv'

df = pd.read_csv(input_file)
if 'Website' not in df.columns:
    df['Website'] = None

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

def find_website(name):
    try:
        url = 'https://www.google.com/search?q=' + name
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        print(soup.find('cite').text)
        return soup.find('cite').text
    except Exception as e:  # Catch any exception during the search
        print(f"Error occurred while searching for {name}: {e}")
        return None  # Return None if there's an error
    return None

for i, row in df.iterrows():
    if pd.isna(row['Website']):
        print(f"Finding website for {row['Golf Course Name']}...")
        df.at[i, 'Website'] = find_website(row['Golf Course Name'])
        #time.sleep(45)  # Increase delay to 60 seconds

df.to_csv(output_file, index=False)
print('Updated spreadsheet saved to', output_file)