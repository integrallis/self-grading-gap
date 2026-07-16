# file: anagram_detector.py

from candidate.impl import AnagramUtility

def find_anagrams(subject, candidates):
    return AnagramUtility.find_anagrams(subject, candidates)

def group_anagrams(words):
    return AnagramUtility.group_anagrams(words)

def is_anagram(text1, text2):
    return AnagramUtility.are_anagrams(text1, text2)
