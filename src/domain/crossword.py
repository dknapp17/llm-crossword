from dataclasses import dataclass

@dataclass
class CrosswordClue:
    text: str # ex: Feline
    length: int # ex: 3
    weekday_num: int # ex: 1
    positional_constraints: dict[int,str] # ex: {1: C} for C _ _

@dataclass
class CrosswordAnswer:
    text: str # ex: DEADHEAT
    length: int
    positional_text: dict[int,str] # ex: {1: DH, 2: E, 3: A, 4: DT}