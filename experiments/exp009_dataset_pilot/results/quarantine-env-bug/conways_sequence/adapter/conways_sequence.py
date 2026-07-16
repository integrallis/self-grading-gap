# file: conways_sequence.py

from candidate.impl import LookAndSay

def look_and_say(term: str) -> str:
    return LookAndSay.next_term(term)

def next_term(term: str) -> str:
    return LookAndSay.next_term(term)
