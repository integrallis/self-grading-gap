# file: conways_sequence.py

from candidate.impl import LookAndSay

def look_and_say(term: str, iterations: int) -> str:
    return LookAndSay.iterate(term, iterations)

def next_term(term: str) -> str:
    return LookAndSay.next_term(term)
