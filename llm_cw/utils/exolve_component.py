import hashlib
import uuid
from pathlib import Path

import streamlit as st

from llm_cw.utils.exolve_ui_bridge import _component


class ExolveComponent:
    def __init__(self, uploaded_file):
        self.puzzle = uploaded_file
        self.state = {}
        self.command = None

        puzzle_bytes = uploaded_file.getvalue()

        exolve_dir = (
            Path(__file__).resolve().parents[2]
            / "app"
            / "static"
            / "exolve"
        )

        puzzle_name = (
            f"{hashlib.sha256(puzzle_bytes).hexdigest()[:16]}.puz"
        )

        (exolve_dir / puzzle_name).write_bytes(puzzle_bytes)

        self.puzzle_path = puzzle_name

    def display(self):
        exolve_js = (
            Path(__file__).resolve().parents[2]
            / "app"
            / "static"
            / "exolve"
            / "exolve-embedder.js"
        )

        self.version = hashlib.md5(exolve_js.read_bytes()).hexdigest()
        self.state = _component(
            data={
                "crossword": self.puzzle_path,
                "version": self.version,
                "command": st.session_state.get("exolve_command"),
            },
        ) or {}
        self.command = None