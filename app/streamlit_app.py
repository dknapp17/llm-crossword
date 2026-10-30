import streamlit as st

import llm_cw.utils.puz_utils as puz_utils
from llm_cw.domain.crossword import SolverClueInput
from llm_cw.retrieval.wordlist import WordList
from llm_cw.solvers.algorithmic_solver import AlgorithmicSolver


# --- load solver once ---
@st.cache_resource
def load_solver():
    with open("data/wordlists/words.txt", "r") as f:
        words = [w.strip() for w in f if w.strip()]

    wordlist = WordList(words)
    return AlgorithmicSolver(wordlist)


solver = load_solver()

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
    selected_clue = puz_utils.display_puzzle(uploaded_file)

    st.subheader("Selected Exolve clue")
    if selected_clue:
        st.write(f"**Clue:** {selected_clue.get('text')}")
        st.write(f"**Length:** {selected_clue.get('answer_length')}")
        st.write(f"**Index:** {selected_clue.get('index')}")
    else:
        st.write("Select a clue in the crossword.")


# --- solver configuration ---
model = st.selectbox("Model", ["Default"], index=0)
retrieval = st.selectbox("Retrieval", ["RAG"], index=0)


# --- run solver for an entire puzzle ---
if st.button("Solve Puzzle"):
    st.write(f"Solving with model={model}, retrieval={retrieval}")


# --- run solver for a single clue ---
if st.button("Solve Clue"):
    clue = SolverClueInput(
        text=clue_text,
        length=int(length),
        positional_constraints=constraints,
    )

    results = solver.solve(clue)

    st.subheader("Results")

    if not results:
        st.write("No matches found.")
    else:
        for r in results:
            st.write(f"• {r.text}")
