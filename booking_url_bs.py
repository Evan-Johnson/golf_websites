import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

input_file = 'new_course_urls.csv'
output_file = 'golf_courses_with_tee_times.csv'

df = pd.read_csv(input_file)
if 'Tee Time URL' not in df.columns:
    df['Tee Time URL'] = None

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

# Update the keywords list based on your requirement
keywords = ["book now", "book your tee time", "tee times", "teetimes", "book your tee-time now", "book a tee time", "public tee times", "book online now", "book online", "reserve your tee time", "book a tee time now", "make a tee time", "reserve your tee time"]

def find_tee_time_link(website_url):
    try:
        res = requests.get(website_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.find_all('a')
        
        for link in links:
            href = link.get('href', '')
            text = link.text.lower()
            for keyword in keywords:
                if keyword.lower() in text or keyword.lower() in href.lower():
                    # Create an absolute URL
                    full_url = urljoin(website_url, href)
                    print(f"Found tee time link: {full_url}")
                    return full_url
        print("No tee time link found.")
        return None
    except Exception as e:
        print(f"Error occurred while searching for tee time link on {website_url}: {e}")
        return None

for i, row in df.iterrows():
    if pd.isna(row['Tee Time URL']) and not pd.isna(row['Website']):
        print(f"Finding tee time link for website {row['Website']}...")
        df.at[i, 'Tee Time URL'] = find_tee_time_link(row['Website'])

df.to_csv(output_file, index=False)
print('Updated spreadsheet with tee time URLs saved to', output_file)

