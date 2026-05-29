from bs4.element import Tag

from src.domain.crossword import (
    AcrossDown,
    CrosswordAnswer,
    CrosswordClue,
    CrosswordClueAnswerPair,
    CrosswordGrid,
    CrosswordGridSquare,
)


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

        clue_text = clue_container.contents[0]

        return clue_text.replace(" : ", "").strip()

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
        squares = self._parse_rows(rows)

        return CrosswordGrid(
            rows=len(rows),
            cols=len(rows[0].find_all("td")) if rows else 0,
            squares=squares,
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
    def _parse_rows(self, rows) -> list[CrosswordGridSquare]:
        squares = []

        for row_idx, row in enumerate(rows):
            squares.extend(self._parse_row(row, row_idx))

        return squares

    def _parse_row(self, row, row_idx: int) -> list[CrosswordGridSquare]:
        cells = row.find_all("td")

        return [
            self._parse_cell(cell, row_idx, col_idx)
            for col_idx, cell in enumerate(cells)
        ]

    # -------------------------
    # Cell level (core logic)
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
            solution_text=None if is_black else self._extract_letter(cell),
            clue_num = self._extract_clue_num(cell)
        )

    # -------------------------
    # Atom logic
    # -------------------------
    def _extract_letter(self, cell) -> str | None:
        letter_div = cell.find("div", class_="letter")
        substr_div = cell.find("div", class_="subst")

        if letter_div:
            return letter_div.text.strip()
        if substr_div:
            return substr_div.text.strip()

        return None
    
    def _extract_clue_num(self, cell) -> int | None:
        num_div = cell.find("div", class_="num")

        if num_div:
            num_text = num_div.text.strip()
            return int(num_text) if num_text else None

        return None
    
    class CrosswordClueParser:
        #TODO: take html and parse clue/answer
        pass