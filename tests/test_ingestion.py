import unittest

from bs4 import BeautifulSoup

from src.pipeline.ingestion import CrosswordGridParser


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
        self.assertEqual(len(grid.squares), 2)
        self.assertEqual(grid.squares[0].solution_text, "A")
        self.assertTrue(grid.squares[1].isblack)


if __name__ == "__main__":
    unittest.main()