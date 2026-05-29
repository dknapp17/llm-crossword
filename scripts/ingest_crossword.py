# TODO: 

# create script to ingest crosswords
# should be able to:
    # update training data
    # update word list with new words

# first pass at using beautiful soup to scrape crosswords

import requests
from bs4 import BeautifulSoup

from src.domain.crossword import SolverAnswer, SolverClueInput
from src.pipeline.ingestion import (
    CrosswordClueAnswerParser,
    CrosswordGridParser,
    # extract_word_from_grid,
)

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

# print(grid.squares[47])
# print(clue_ans_html)
print(f"first clue: {clue_answer_pairs[0].crossword_clue}")
print(f"first answer: {clue_answer_pairs[0].crossword_answer}")

print(f"square in row 3, column 6: {grid.squares[2][5]}")

print(f"first square of clue 1: {grid.get_by_clue_num(1)}")

# now we have a grid (collection of squares and a collection of clue answer pairs)
# use these together to get SolverClueInput and SolverAnswer
print(f"parsing a {grid.rows} by {grid.cols} grid")
for pair in clue_answer_pairs:
    #TODO: move this into a function and reuse logic for across and down
    clue_num = pair.crossword_clue.clue_num
    if pair.crossword_clue.across_down == 'across':
        len_counter = 1
        positional_text = {}
        is_valid = True
        print("parsing grid across")
        print(f"parsing clue {pair.crossword_clue.clue_num}")
        print(f"first letter of clue: {grid.get_by_clue_num(clue_num)}")
        cur_square = grid.get_by_clue_num(clue_num=clue_num)
        cur_row, cur_col = cur_square.row, cur_square.col
        positional_text[0] = cur_square.solution_text

        while is_valid:
            cur_col += 1

            if cur_col >= grid.cols:
                break

            cur_square = grid.squares[cur_row][cur_col]

            if cur_square.isblack:
                break

            len_counter += 1
            positional_text[len_counter] = cur_square.solution_text

        # print(f"answer length: {len_counter}")
        # print(f"positional text: {positional_text}")
        solver_answer = SolverAnswer(
            text=pair.crossword_answer.text,
            length=len_counter,
            positional_text=positional_text
        )
        solver_clue_input = SolverClueInput(
            text=pair.crossword_clue.text,
            length=len_counter,
            weekday_num=0, # add puzzle metadata later
            positional_constraints={} # add possible positional constraints later
        )
        print(solver_answer)
        print(solver_clue_input)

            





    else:
        pass
        # print("parsing grid down")
        # print(f"parsing clue {pair.crossword_clue.clue_num}")

