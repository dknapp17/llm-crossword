# TODO: 

# create script to ingest crosswords
# should be able to:
    # update training data
    # update word list with new words

# first pass at using beautiful soup to scrape crosswords

import requests
from bs4 import BeautifulSoup

from src.pipeline.ingestion import CrosswordGridParser

url = 'https://www.xwordinfo.com/Crossword?date=4/19/2026'
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120 Safari/537.36"
    )
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, features='html.parser')

puz_html = soup.find("table", id="PuzTable")

# step1: parse clue, answer key value pairs
# step2: parse grid to get locations of all squares
# step3: use clue/answer and grid objects to get CrosswordClue and CrosswordAnswer pairs
    # ex: 1 across. find square 1 and get result of that square 
    # and all squares to the right until black or border
    # ex: 1 down. find square 1 and get result of that square
    # and all squares below until black or border

# parse puzzle
parser = CrosswordGridParser()
grid = parser.parse(puz_html)

print(grid.squares[47])
