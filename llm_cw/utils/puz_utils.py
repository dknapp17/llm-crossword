
import hashlib
from pathlib import Path

import puz
import streamlit as st

import atexit


def load_puz_file(file_bytes: bytes) -> puz.Puzzle:
    return puz.load(file_bytes)


def display_puzzle(uploaded_file) -> None:
    puzzle_bytes = uploaded_file.getvalue()

    # Save the puzzle beside the Exolve embedder.
    exolve_dir = (
        Path(__file__).resolve().parents[2]
        / "app"
        / "static"
        / "exolve"
    )
    puzzle_name = f"{hashlib.sha256(puzzle_bytes).hexdigest()[:16]}.puz"
    # Remove files from previous uploads.
    for old_puzzle in exolve_dir.glob("*.puz"):
        if old_puzzle.name != puzzle_name:
            old_puzzle.unlink()

    (exolve_dir / puzzle_name).write_bytes(puzzle_bytes)
    (exolve_dir / puzzle_name).write_bytes(puzzle_bytes)

    # Load the interactive Exolve player.
    player_url = (
        f"/app/static/exolve/exolve-embedder.html"
        f"?crossword={puzzle_name}"
    )
    st.iframe(player_url, height=800)

def cleanup_puz_files() -> None:
    exolve_dir = (
        Path(__file__).resolve().parents[2]
        / "app"
        / "static"
        / "exolve"
    )
    for puzzle_file in exolve_dir.glob("*.puz"):
        puzzle_file.unlink()


atexit.register(cleanup_puz_files)