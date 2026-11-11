from pathlib import Path

import streamlit as st

from llm_cw.utils.exolve_component import ExolveComponent

st.title("🧩 Crossword Solver (Algorithmic Baseline)")


# --- inputs ---
clue_text = st.text_input("Clue", "Feline pet")
length = st.number_input("Length", min_value=2, max_value=20, value=3)

constraint_input = st.text_input(
    "Constraints (format: 0:C,2:T)",
    ""
)


# --- parse constraints ---
def parse_constraints(text):
    if not text.strip():
        return None

    constraints = {}
    for part in text.split(","):
        if ":" in part:
            idx, letter = part.split(":")
            constraints[int(idx.strip())] = letter.strip()

    return constraints


constraints = parse_constraints(constraint_input)


# --- upload .puz file ---
uploaded_file = st.file_uploader("Upload .puz file", type=["puz"])

if uploaded_file is not None:
    exolve = ExolveComponent(uploaded_file)
    exolve.display()

# --- solver configuration ---
model = st.selectbox("Model", ["Default"], index=0)
retrieval = st.selectbox("Retrieval", ["RAG"], index=0)


# --- run solver for an entire puzzle ---

if st.button("Solve Puzzle", disabled=uploaded_file is None):
    Path("solve_requested.txt").write_text("solve")