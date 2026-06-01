import unittest

from bs4 import BeautifulSoup

from src.domain.crossword import AcrossDown, CrosswordGridSquare
from src.infrastructure.ingestion import (
    CrosswordClueAnswerParser,
    CrosswordGridParser,
    extract_word_from_grid,
)


class TestCrosswordGridParser(unittest.TestCase):

    def setUp(self):
        self.parser = CrosswordGridParser()

    # -------------------------
    # Helpers
    # -------------------------
    def make_cell(self, html: str):
        return BeautifulSoup(html, "html.parser").find("td")

    def make_row(self, html: str):
        return BeautifulSoup(html, "html.parser").find("tr")

    def make_table(self, html: str):
        return BeautifulSoup(html, "html.parser").find("table")

    # -------------------------
    # _validate_table
    # -------------------------
    def test_validate_table_valid(self):
        table = self.make_table("<table></table>")
        self.parser._validate_table(table)  # should not raise

    def test_validate_table_invalid(self):
        with self.assertRaises(ValueError):
            self.parser._validate_table(
                BeautifulSoup("<div></div>", "html.parser").find("div")
            )

    # -------------------------
    # _extract_letter
    # -------------------------
    def test_extract_letter_letter_div(self):
        cell = self.make_cell(
            "<td><div class='letter'>A</div></td>"
        )
        self.assertEqual(self.parser._extract_letter(cell), "A")

    def test_extract_letter_subst_div(self):
        cell = self.make_cell(
            "<td><div class='subst'>B</div></td>"
        )
        self.assertEqual(self.parser._extract_letter(cell), "B")

    def test_extract_letter_none(self):
        cell = self.make_cell("<td></td>")
        self.assertIsNone(self.parser._extract_letter(cell))

    # -------------------------
    # _extract_clue_num
    # -------------------------
    def test_extract_clue_num_present(self):
        cell = self.make_cell(
            "<td><div class='num'>12</div></td>"
        )
        self.assertEqual(self.parser._extract_clue_num(cell), 12)

    def test_extract_clue_num_empty(self):
        cell = self.make_cell(
            "<td><div class='num'></div></td>"
        )
        self.assertIsNone(self.parser._extract_clue_num(cell))

    def test_extract_clue_num_missing(self):
        cell = self.make_cell("<td></td>")
        self.assertIsNone(self.parser._extract_clue_num(cell))

    # -------------------------
    # _parse_cell
    # -------------------------
    def test_parse_cell_black(self):
        cell = self.make_cell(
            "<td class='black'></td>"
        )
        result = self.parser._parse_cell(cell, 0, 0)

        self.assertTrue(result.isblack)
        self.assertIsNone(result.solution_text)

    def test_parse_cell_white(self):
        cell = self.make_cell(
            "<td><div class='letter'>C</div><div class='num'>1</div></td>"
        )
        result = self.parser._parse_cell(cell, 0, 0)

        self.assertFalse(result.isblack)
        self.assertEqual(result.solution_text, "C")
        self.assertEqual(result.clue_num, 1)
        self.assertEqual(result.row, 0)
        self.assertEqual(result.col, 0)

    # -------------------------
    # _parse_row
    # -------------------------
    def test_parse_row(self):
        row = self.make_row("""
        <tr>
            <td><div class='letter'>A</div></td>
            <td class='black'></td>
        </tr>
        """)

        squares = self.parser._parse_row(row, 0)

        self.assertEqual(len(squares), 2)
        self.assertEqual(squares[0].solution_text, "A")
        self.assertTrue(squares[1].isblack)

    # -------------------------
    # _parse_rows
    # -------------------------
    def test_parse_rows(self):
        html = """
        <table>
            <tr>
                <td><div class='letter'>A</div></td>
            </tr>
            <tr>
                <td class='black'></td>
            </tr>
        </table>
        """

        soup = BeautifulSoup(html, "html.parser")
        rows = soup.find_all("tr")

        squares = self.parser._parse_rows(rows)

        self.assertEqual(len(squares), 2)

    # -------------------------
    # parse (integration)
    # -------------------------
    def test_parse_full_table(self):
        html = """
        <table>
            <tr>
                <td><div class='letter'>A</div><div class='num'>1</div></td>
                <td class='black'></td>
            </tr>
        </table>
        """

        table = BeautifulSoup(html, "html.parser").find("table")

        grid = self.parser.parse(table)

        self.assertEqual(grid.rows, 1)
        self.assertEqual(grid.cols, 2)
        self.assertEqual(len(grid.squares), 1)
        self.assertEqual(grid.squares[0][0].solution_text, "A")
        self.assertTrue(grid.squares[0][1].isblack)

class TestCrosswordClueParser(unittest.TestCase):

    def setUp(self):
        self.parser = CrosswordClueAnswerParser()

    # -------------------------
    # Helpers
    # -------------------------
    def make_soup(self, html: str):
        return BeautifulSoup(html, "html.parser")

    # -------------------------
    # _extract_clue_text
    # -------------------------
    def test_extract_clue_text(self):

        soup = self.make_soup("""
        <div>
            Feline :
            <a href="/Finder?w=CAT">CAT</a>
        </div>
        """)

        div = soup.find("div")

        result = self.parser._extract_clue_text(div)

        self.assertEqual(result, "Feline")

    # -------------------------
    # _extract_answer_text
    # -------------------------
    def test_extract_answer_text(self):

        soup = self.make_soup("""
        <div>
            Feline :
            <a href="/Finder?w=CAT">CAT</a>
        </div>
        """)

        div = soup.find("div")

        result = self.parser._extract_answer_text(div)

        self.assertEqual(result, "CAT")

    def test_extract_answer_text_missing_link(self):

        soup = self.make_soup("""
        <div>
            Feline
        </div>
        """)

        div = soup.find("div")

        with self.assertRaises(ValueError):
            self.parser._extract_answer_text(div)

    # -------------------------
    # _parse_direction
    # -------------------------
    def test_parse_direction_across(self):

        html = """
        <div id="ACluesPan">
            <div class="numclue">
                <div>1</div>
                <div>
                    Feline :
                    <a href="/Finder?w=CAT">CAT</a>
                </div>

                <div>2</div>
                <div>
                    Canine :
                    <a href="/Finder?w=DOG">DOG</a>
                </div>
            </div>
        </div>
        """

        soup = self.make_soup(html)

        direction_div = soup.find("div", id="ACluesPan")

        results = self.parser._parse_direction(
            direction_div,
            AcrossDown.ACROSS,
        )

        self.assertEqual(len(results), 2)

        first_pair = results[0]

        self.assertEqual(
            first_pair.crossword_clue.text,
            "Feline",
        )

        self.assertEqual(
            first_pair.crossword_answer.text,
            "CAT",
        )

        self.assertEqual(
            first_pair.crossword_clue.clue_num,
            1,
        )

        self.assertEqual(
            first_pair.crossword_clue.across_down,
            AcrossDown.ACROSS,
        )

    def test_parse_direction_none(self):

        results = self.parser._parse_direction(
            None,
            AcrossDown.DOWN,
        )

        self.assertEqual(results, [])

    def test_parse_direction_missing_numclue(self):

        soup = self.make_soup("""
        <div id="DCluesPan"></div>
        """)

        direction_div = soup.find("div")

        results = self.parser._parse_direction(
            direction_div,
            AcrossDown.DOWN,
        )

        self.assertEqual(results, [])

    # -------------------------
    # parse
    # -------------------------
    def test_parse_full_cluebox(self):

        html = """
        <div class="cluebox">

            <div id="ACluesPan">
                <div class="numclue">
                    <div>1</div>
                    <div>
                        Feline :
                        <a href="/Finder?w=CAT">CAT</a>
                    </div>
                </div>
            </div>

            <div id="DCluesPan">
                <div class="numclue">
                    <div>2</div>
                    <div>
                        Canine :
                        <a href="/Finder?w=DOG">DOG</a>
                    </div>
                </div>
            </div>

        </div>
        """

        soup = self.make_soup(html)

        cluebox = soup.find("div", class_="cluebox")

        results = self.parser.parse(cluebox)

        self.assertEqual(len(results), 2)

        across_pair = results[0]
        down_pair = results[1]

        self.assertEqual(
            across_pair.crossword_clue.text,
            "Feline",
        )

        self.assertEqual(
            across_pair.crossword_answer.text,
            "CAT",
        )

        self.assertEqual(
            across_pair.crossword_clue.across_down,
            AcrossDown.ACROSS,
        )

        self.assertEqual(
            down_pair.crossword_clue.text,
            "Canine",
        )

        self.assertEqual(
            down_pair.crossword_answer.text,
            "DOG",
        )

        self.assertEqual(
            down_pair.crossword_clue.across_down,
            AcrossDown.DOWN,
        )

class FakeGrid:
    def __init__(self, squares):
        self.squares = squares
        self.rows = len(squares)
        self.cols = len(squares[0])

    def get(self, row, col):
        return self.squares[row][col]


class TestExtractWordFromGrid(unittest.TestCase):

    def test_across_simple_word(self):

        grid = FakeGrid([
            [
                CrosswordGridSquare(0, 0, False, "C"),
                CrosswordGridSquare(0, 1, False, "A"),
                CrosswordGridSquare(0, 2, False, "T"),
            ]
        ])

        length, positional = extract_word_from_grid(
            grid,
            start_row=0,
            start_col=0,
            delta_row=0,
            delta_col=1,
        )

        self.assertEqual(length, 3)
        self.assertEqual(positional, {
            0: "C",
            1: "A",
            2: "T",
        })

    def test_stops_at_black_square(self):

        grid = FakeGrid([
            [
                CrosswordGridSquare(0, 0, False, "C"),
                CrosswordGridSquare(0, 1, True, None),
                CrosswordGridSquare(0, 2, False, "T"),
            ]
        ])

        length, positional = extract_word_from_grid(
            grid,
            start_row=0,
            start_col=0,
            delta_row=0,
            delta_col=1,
        )

        self.assertEqual(length, 1)
        self.assertEqual(positional, {
            0: "C"
        })

    def test_down_word(self):

        grid = FakeGrid([
            [CrosswordGridSquare(0, 0, False, "C")],
            [CrosswordGridSquare(1, 0, False, "A")],
            [CrosswordGridSquare(2, 0, False, "T")],
        ])

        length, positional = extract_word_from_grid(
            grid,
            start_row=0,
            start_col=0,
            delta_row=1,
            delta_col=0,
        )

        self.assertEqual(length, 3)
        self.assertEqual(positional, {
            0: "C",
            1: "A",
            2: "T",
        })

    def test_single_cell_word(self):

        grid = FakeGrid([
            [CrosswordGridSquare(0, 0, False, "A")]
        ])

        length, positional = extract_word_from_grid(
            grid,
            start_row=0,
            start_col=0,
            delta_row=0,
            delta_col=1,
        )

        self.assertEqual(length, 1)
        self.assertEqual(positional, {0: "A"})
if __name__ == "__main__":
    unittest.main()