import base64
import subprocess

import puz
import streamlit as st


def load_puz_file(file_bytes: bytes) -> puz.Puzzle:
    return puz.load(file_bytes)


def display_puzzle(uploaded_file) -> None:
    result = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "scripts/puz_viewer.py",
            "-f",
            "puz",
        ],
        input=uploaded_file.getvalue(),
        capture_output=True,
        check=True,
    )

    html = result.stdout.decode("utf-8")
    encoded_html = base64.b64encode(html.encode("utf-8")).decode("ascii")

    st.iframe(
        f"data:text/html;base64,{encoded_html}",
        height=800,
    )