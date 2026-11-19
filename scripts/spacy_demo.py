import spacy

nlp = spacy.load("en_core_web_sm")

clues = [
    "Officially, the Empire State Building has 102 of them",
    "Some quick chemical assessments",
    "Ancient symbols of royalty",
    "Feline pet",
    "Feline pets",
    "Backwards",
    "Flat",
    "Stupors",
    "Read, as a bar code", # could be past or present
    "Ending of some D.C. addresses", # while addresses is plural, Ending is key word
    "Board at a nail salon",
    "Housebroken, say",
    "Fixture at many a cash-only restaurant",
    "Mate", # could be noun or verb
    "Trap", # could be noun or verb
    """Like the sounds "m", "n", and "ng," in English""", # answer should be adjective
    """ Emmitt and kin, in "Zootopia" """,
    "Like some meats", # answer should be adjective
    "Picks up",
    "Some medical assistants, in brief", # answer should be abbreviated
    "Relating to Leo XIV, e.g.",
    "Profs' right hands", # abbreviated and plural
    "Animation frame",
    "Aggrieved",
    "Take care of", # present tense
    "Lose to gravity",
    "Like some of the French crown jewels in 2025",
    "Certain jazz combo",
    "Cropped up", # past tense
    "Musical collection, say", # answer here is Tonys...
    "Clog or loafer", # singular answer
    "Clog and loafer, for two" # plural answer
    """Freud conceived of a "super" one""",
    "Talks, talks, talks",
    """Neither's partner""",
    "Unconsciously make noise?",
    "Like some apartment appliances",
    "Goody bag item",
    "If's partner, in coding",
    "Defeats by a hair",
    "Foreign spies, e.g."


]

for clue in clues:
    doc = nlp(clue)

    print(f"\nClue: {clue}")

    for token in doc:
        print(
            f'text: {token.text}|',
            f'part of speech: {token.pos_}|',
            f'dep: {token.dep_}|',
            f'tag: {token.tag_}|',
            f'morphology: {token.morph}|',
            f'lemma: {token.lemma_}|',
        )