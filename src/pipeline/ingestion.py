from bs4.element import Tag

from src.domain.crossword import (
    CrosswordGrid,
    CrosswordGridSquare,
)


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