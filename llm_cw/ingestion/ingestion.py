from datetime import datetime

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from llm_cw.domain.crossword import (
    AcrossDown,
    CrosswordAnswer,
    CrosswordClue,
    CrosswordClueAnswerPair,
    CrosswordGrid,
    CrosswordGridSquare,
    CrosswordPuzzleData,
    SolverAnswer,
    SolverClueInput,
)
from llm_cw.domain.documents import CrosswordDocument


class CrosswordClueAnswerParser:

    def parse(
        self,
        html_cluebox: Tag,
    ) -> list[CrosswordClueAnswerPair]:

        across_pairs = self._parse_direction(
            html_cluebox.find("div", id="ACluesPan"),
            AcrossDown.ACROSS,
        )

        down_pairs = self._parse_direction(
            html_cluebox.find("div", id="DCluesPan"),
            AcrossDown.DOWN,
        )

        return across_pairs + down_pairs

    # -------------------------
    # Direction level
    # -------------------------
    def _parse_direction(
        self,
        direction_div: Tag,
        across_down: AcrossDown,
    ) -> list[CrosswordClueAnswerPair]:

        if direction_div is None:
            return []

        numclue_div = direction_div.find("div", class_="numclue")

        if numclue_div is None:
            return []

        children = numclue_div.find_all("div", recursive=False)

        clue_answer_pairs = []

        for idx in range(0, len(children), 2):

            clue_num = int(children[idx].text.strip())

            clue_container = children[idx + 1]

            clue_text = self._extract_clue_text(clue_container)
            answer_text = self._extract_answer_text(clue_container)

            crossword_clue = CrosswordClue(
                text=clue_text,
                across_down=across_down,
                clue_num=clue_num,
            )

            crossword_answer = CrosswordAnswer(
                text=answer_text,
                across_down=across_down,
                clue_num=clue_num,
            )

            clue_answer_pairs.append(
                CrosswordClueAnswerPair(
                    crossword_clue=crossword_clue,
                    crossword_answer=crossword_answer,
                )
            )

        return clue_answer_pairs

    # -------------------------
    # Atom logic
    # -------------------------
    def _extract_clue_text(
        self,
        clue_container: Tag,
    ) -> str:

        clue_text = clue_container.get_text().strip()
        
        return clue_text.rsplit(":", 1)[0].strip()

    def _extract_answer_text(
        self,
        clue_container: Tag,
    ) -> str:

        answer_link = clue_container.find("a")

        if answer_link is None:
            raise ValueError("Could not find answer link")

        return answer_link.text.strip()


class CrosswordGridParser:

    def parse(self, html_table: Tag) -> CrosswordGrid:

        self._validate_table(html_table)

        rows = html_table.find_all("tr")

        parsed_rows = self._parse_rows(rows)

        return CrosswordGrid(
            squares=parsed_rows,
        )

    # -------------------------
    # Validation
    # -------------------------
    def _validate_table(self, table: Tag) -> None:

        if table.name != "table":
            raise ValueError("Expected a <table> element")

    # -------------------------
    # Row level
    # -------------------------
    def _parse_rows(
        self,
        rows,
    ) -> list[list[CrosswordGridSquare]]:

        return [
            self._parse_row(row, row_idx)
            for row_idx, row in enumerate(rows)
        ]

    def _parse_row(
        self,
        row,
        row_idx: int,
    ) -> list[CrosswordGridSquare]:

        cells = row.find_all("td")

        return [
            self._parse_cell(cell, row_idx, col_idx)
            for col_idx, cell in enumerate(cells)
        ]

    # -------------------------
    # Cell level
    # -------------------------
    def _parse_cell(
        self,
        cell,
        row_idx: int,
        col_idx: int,
    ) -> CrosswordGridSquare:

        is_black = "black" in cell.get("class", [])

        return CrosswordGridSquare(
            row=row_idx,
            col=col_idx,
            isblack=is_black,
            solution_text=(
                None
                if is_black
                else self._extract_letter(cell)
            ),
            clue_num=self._extract_clue_num(cell),
        )

    # -------------------------
    # Atom logic
    # -------------------------
    def _extract_letter(
        self,
        cell,
    ) -> str | None:

        letter_div = cell.find("div", class_="letter")
        substr_div = cell.find("div", class_="subst")

        if letter_div:
            return letter_div.text.strip()

        if substr_div:
            return substr_div.text.strip()

        return None

    def _extract_clue_num(
        self,
        cell,
    ) -> int | None:

        num_div = cell.find("div", class_="num")

        if num_div:
            num_text = num_div.text.strip()
            return int(num_text) if num_text else None

        return None



def extract_word_from_grid(
    grid: CrosswordGrid,
    start_row: int,
    start_col: int,
    delta_row: int,
    delta_col: int,
):
    row, col = start_row, start_col

    positional_text = {}
    length = 0

    square = grid.get(row, col)
    positional_text[f"idx_{length}"] = square.solution_text

    while True:
        row += delta_row
        col += delta_col

        if row < 0 or row >= grid.rows:
            break
        if col < 0 or col >= grid.cols:
            break

        square = grid.get(row, col)

        if square.isblack:
            break

        length += 1
        positional_text[f"idx_{length}"] = square.solution_text

    return length + 1, positional_text

def construct_url_from_date(puzzle_date: datetime) -> str:
    year = str(puzzle_date.year)
    month = str(puzzle_date.month)
    day = str(puzzle_date.day)

    return f"https://www.xwordinfo.com/Crossword?date={month}/{day}/{year}"

def construct_puzzle_data_from_date(puzzle_date: datetime) -> CrosswordPuzzleData:
    return CrosswordPuzzleData(
        puzzle_date=puzzle_date,
        puzzle_dow=puzzle_date.weekday(),
        puzzle_url=construct_url_from_date(puzzle_date)
    )

def fetch_crossword_page(
    url: str,
    session: requests.Session | None = None,
) -> BeautifulSoup:
    """
    Fetch crossword HTML and return parsed BeautifulSoup object.
    Uses a session if provided (recommended for batch ingestion).
    """

    session = session or requests.Session()

    try:
        response = session.get(
            url,
            headers=HEADERS,
            timeout=15,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch crossword page: {url}") from e

    return BeautifulSoup(response.text, features="html.parser")

def build_docs(clue_answer_pairs: list[CrosswordClueAnswerPair],
               grid: CrosswordGrid,
               puzzle_data: CrosswordPuzzleData
    ) -> list[CrosswordDocument]:
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

        docs.append(to_document(solver_clue_input, solver_answer, puzzle_data))
        
    return docs

def to_document(
        clue: SolverClueInput,
        answer: SolverAnswer,
        puzzle_data: CrosswordPuzzleData
    ) -> CrosswordDocument:
    return CrosswordDocument(
        clue_data=clue,
        answer_data=answer,
        puzzle_data=puzzle_data
    )

def ingest_crossword(
    puzzle_date: datetime,
) -> list[CrosswordDocument]:

    # 1. build metadata
    puzzle_data = construct_puzzle_data_from_date(puzzle_date)
    url = puzzle_data.puzzle_url

    # 2. fetch HTML
    soup = fetch_crossword_page(url)

    # 3. extract DOM pieces
    puz_html = soup.find("table", id="PuzTable")
    clue_ans_html = soup.find("div", id="CPHContent_ClueBox")

    if puz_html is None or clue_ans_html is None:
        raise ValueError("Malformed crossword page")

    # 4. parse domain objects
    clue_answer_pairs = CrosswordClueAnswerParser().parse(clue_ans_html)
    grid = CrosswordGridParser().parse(puz_html)

    # 5. build documents
    return build_docs(
        clue_answer_pairs=clue_answer_pairs,
        grid=grid,
        puzzle_data=puzzle_data,
    )

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120 Safari/537.36"
    )
}