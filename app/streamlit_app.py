import streamlit as st

from llm_cw.domain.crossword import CrosswordClue
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


# --- run solver ---
if st.button("Solve"):
    clue = CrosswordClue(
        text=clue_text,
        length=int(length),
        weekday_num=0,
        positional_constraints=constraints
    )

    results = solver.solve(clue)

    st.subheader("Results")

    if not results:
        st.write("No matches found.")
    else:
        for r in results:
            st.write(f"• {r.text}")