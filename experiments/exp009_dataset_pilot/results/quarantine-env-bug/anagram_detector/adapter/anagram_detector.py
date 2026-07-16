# file: anagram_detector.py

from candidate.impl import AnagramDetector

def find_anagrams(subject, candidates):
    return AnagramDetector.find_anagrams(subject, candidates)

def group_anagrams(words):
    return AnagramDetector.group_anagrams(words)

def is_anagram(text1, text2):
    return AnagramDetector.are_anagrams(text1, text2)
