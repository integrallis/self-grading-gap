# file: anagram_detector.py
from candidate.impl import AnagramTool

def find_anagrams(subject, candidates):
    return AnagramTool.find_anagrams(subject, candidates)

def group_anagrams(word_list):
    return AnagramTool.group_anagrams(word_list)

def is_anagram(text1, text2):
    return AnagramTool.are_anagrams(text1, text2)
