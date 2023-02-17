# IMPORTANT: command line arguments need to be used!!!
# all lower case
# 1) is the city name e.g. berlin, hamburg
# 2) is the wohnung or haus
# 3) save as scv? then write scv.

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re
import json
import sys


# This block is used to get the max_page number. This number is
# then used in the for loop.
city = sys.argv[1]
real_estate = sys.argv[2]
csv = sys.argv[3]

url=f"https://www.immonet.de/{city}/{real_estate}-mieten-seite0.html"
print(url)
url_read_out = requests.get(url)
content = BeautifulSoup(url_read_out.content, "html.parser")
doc = content.find_all("li", "pagination-item") 
number_page = re.search("data-enum=\"[0-9][0-9]+\"", str(doc)).group(0)
max_page = int(re.search("\d+", number_page).group(0))

loop_count = 0
for i in range(max_page):
    loop_count +=1
    time.sleep(2) # scrap every 2 seconds
    url=f"https://www.immonet.de/{city}/{real_estate}-mieten-seite{i}.html"
    url_read_out = requests.get(url)
    content = BeautifulSoup(url_read_out.content, "html.parser")
    doc = content.body.find(string = re.compile("utag_data")) # the target dictionary has the name "utag_data"
    data = json.loads(re.search('({.+})', doc).group(0).replace("'", '"')) # extract the target dictionary
    df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in data.items()])).dropna(axis=1) # create a pandas dataframe. ignore arrays of different length
    if i == 0:
        complete_session_df = df

    complete_session_df = pd.concat([complete_session_df, df])
print("Number of Scraped Pages:", loop_count)

if sys.argv[3] == csv:
    complete_session_df.to_csv(f'immonet')
