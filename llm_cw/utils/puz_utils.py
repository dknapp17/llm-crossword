import puz


def load_puz_file(file_bytes: bytes) -> puz.Puzzle:
    return puz.load(file_bytes)


