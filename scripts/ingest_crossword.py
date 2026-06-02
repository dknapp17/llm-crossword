# TODO: 

# create script to ingest crosswords
# should be able to:
    # update training data
    # update word list with new words

# first pass at using beautiful soup to scrape crosswords

from datetime import datetime

import requests
from bs4 import BeautifulSoup

from llm_cw.domain.documents import CrosswordDocument
from llm_cw.infrastructure.ingestion import (
    HEADERS,
    CrosswordClueAnswerParser,
    CrosswordGridParser,
    build_docs,
    construct_puzzle_data_from_date,
    construct_url_from_date,
)

# TODO:
# construct url from date
# construct headers from date
# create soup

# parse metadata from soup
puzzle_date = datetime(2026, 4, 19)
url = construct_url_from_date(puzzle_date)

puzzle_data = construct_puzzle_data_from_date(puzzle_date)

response = requests.get(url, headers=HEADERS)

soup = BeautifulSoup(response.text, features='html.parser')

puz_html = soup.find("table", id="PuzTable")

clue_ans_html = soup.find("div", id="CPHContent_ClueBox")

# parse puzzle
clue_answer_parser = CrosswordClueAnswerParser()
clue_answer_pairs = clue_answer_parser.parse(clue_ans_html)

grid_parser = CrosswordGridParser()
grid = grid_parser.parse(puz_html)

# now we have a grid (collection of squares and a collection of clue answer pairs)
# use these together to get SolverClueInput and SolverAnswer
print(f"parsing a {grid.rows} by {grid.cols} grid")
docs = build_docs(clue_answer_pairs,
                  grid,
                  puzzle_data)

CrosswordDocument.bulk_insert(docs)