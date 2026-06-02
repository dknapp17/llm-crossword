# TODO: 

# create script to ingest crosswords
# should be able to:
    # update training data
    # update word list with new words

# first pass at using beautiful soup to scrape crosswords

from datetime import datetime

import requests
from bs4 import BeautifulSoup

from llm_cw.domain.crossword import SolverAnswer, SolverClueInput
from llm_cw.infrastructure.ingestion import (
    CrosswordClueAnswerParser,
    CrosswordGridParser,
    construct_puzzle_data_from_date,
    construct_url_from_date,
    extract_word_from_grid,
    to_document,
)

# TODO:
# construct url from date
# construct headers from date
# create soup

# parse metadata from soup
puzzle_date = datetime(2026, 4, 19)
url = construct_url_from_date(puzzle_date)

puzzle_data = construct_puzzle_data_from_date(puzzle_date)

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

clue_ans_html = soup.find("div", id="CPHContent_ClueBox")

# step1: parse clue, answer key value pairs
# step2: parse grid to get locations of all squares
# step3: use clue/answer and grid objects to get CrosswordClue and CrosswordAnswer pairs
    # ex: 1 across. find square 1 and get result of that square 
    # and all squares to the right until black or border
    # ex: 1 down. find square 1 and get result of that square
    # and all squares below until black or border

# parse puzzle
clue_answer_parser = CrosswordClueAnswerParser()
clue_answer_pairs = clue_answer_parser.parse(clue_ans_html)

grid_parser = CrosswordGridParser()
grid = grid_parser.parse(puz_html)

print(f"first clue: {clue_answer_pairs[0].crossword_clue}")
print(f"first answer: {clue_answer_pairs[0].crossword_answer}")

print(f"square in row 3, column 6: {grid.squares[2][5]}")

print(f"first square of clue 1: {grid.get_by_clue_num(1)}")

# now we have a grid (collection of squares and a collection of clue answer pairs)
# use these together to get SolverClueInput and SolverAnswer
print(f"parsing a {grid.rows} by {grid.cols} grid")
docs = []
for pair in clue_answer_pairs:
    clue_num = pair.crossword_clue.clue_num
    start_square = grid.get_by_clue_num(clue_num)

    if pair.crossword_clue.across_down == "across":

        length, positional_text = extract_word_from_grid(
            grid,
            start_square.row,
            start_square.col,
            delta_row=0,
            delta_col=1,
        )


    else:
        length, positional_text = extract_word_from_grid(
            grid,
            start_square.row,
            start_square.col,
            delta_row=1,
            delta_col=0,
        )

    solver_answer = SolverAnswer(
            text=pair.crossword_answer.text,
            length=length,
            positional_text=positional_text,
        )

    solver_clue_input = SolverClueInput(
        text=pair.crossword_clue.text,
        length=length,
        positional_constraints={},
    )

    print(solver_clue_input, solver_answer)

    docs.append(to_document(solver_clue_input, solver_answer, puzzle_data))
# CrosswordDocument.bulk_insert(docs)