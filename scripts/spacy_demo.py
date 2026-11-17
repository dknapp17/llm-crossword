import spacy

nlp = spacy.load("en_core_web_sm")

clues = [
    "Officially, the Empire State Building has 102 of them",
    "Some quick chemical assessments",
    "What a pilot does",
    "Feline pet",
    "Feline pets",
]

for clue in clues:
    doc = nlp(clue)

    print(f"\nClue: {clue}")

    for token in doc:
        print(
            token.text,
            token.pos_,
            token.dep_,
            token.morph,
        )