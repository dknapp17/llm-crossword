# TODO: 

# create script to ingest crosswords
# should be able to:
    # update training data
    # update word list with new words

# first pass at using beautiful soup to scrape crosswords

import requests
from bs4 import BeautifulSoup

url = 'https://www.xwordinfo.com/Crossword?date=5/23/2026'
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120 Safari/537.36"
    )
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, features='html.parser')

print(soup.prettify())

# step 1: parse clue, answer key value pairs
# step 2: parse puzzle to get letter constraints
    # ex: 1 across. find square 1 and get result of that square 
    # and all squares to the right until black or border
    # ex: 1 down. find square 1 and get result of that square
    # and all squares below until black or border