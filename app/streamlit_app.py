from pathlib import Path

import streamlit as st

from llm_cw.utils.exolve_component import ExolveComponent


@st.fragment(run_every="1s")
def display_solver_log():
    log_file = Path("solver_log.txt")

    with st.container(height=600, border=True):
        if log_file.exists():
            messages = log_file.read_text(encoding="utf-8").splitlines()

            for message in messages:
                st.write(message)

st.title("🧩 Crossword Solver (Algorithmic Baseline)")
left_col, right_col = st.columns([2, 1])
with left_col:
    # --- upload .puz file ---
    uploaded_file = st.file_uploader("Upload .puz file", type=["puz"])

    if uploaded_file is not None:
        exolve = ExolveComponent(uploaded_file)
        exolve.display()

with right_col:
    st.subheader("Solver Log")
    display_solver_log()

# --- solver configuration ---
model = st.selectbox("Model", ["Default"], index=0)
retrieval = st.selectbox("Retrieval", ["RAG"], index=0)


# --- run solver for an entire puzzle ---

if st.button("Solve Puzzle", disabled=uploaded_file is None):
    Path("solve_requested.txt").write_text("solve")