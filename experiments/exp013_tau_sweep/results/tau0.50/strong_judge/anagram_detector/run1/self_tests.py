import pytest
from solution import detect_anagram, find_anagrams, group_anagrams

# Test suite for the anagram detection functionality

# US-1: Detect whether two texts are anagrams
def test_anagram_detection_different_words():
    assert detect_anagram("listen", "silent") is True  # both contain 'eilnst'
    assert detect_anagram("cat", "tac") is True  # both contain 'act'
    assert detect_anagram("ab", "ba") is True  # both contain 'ab'

def test_anagram_detection_not_anagrams():
    assert detect_anagram("hello", "world") is False  # different letters
    assert detect_anagram("aab", "abb") is False  # 'a' occurs different number of times

def test_anagram_detection_case_insensitivity():
    assert detect_anagram("Cat", "tac") is True  # 'cat' and 'tac' are anagrams

def test_anagram_detection_not_itself():
    assert detect_anagram("word", "word") is False  # identical words
    assert detect_anagram("A", "a") is False  # same letter differing only in case
    assert detect_anagram("", "") is False  # both are empty texts
    assert detect_anagram("a", "a") is False  # identical single letters

def test_anagram_detection_ignoring_spaces():
    assert detect_anagram("Dormitory", "Dirty Room") is True  # ignoring spaces

def test_anagram_detection_ignoring_punctuation():
    assert detect_anagram("Astronomer", "Moon starer!") is True  # ignoring punctuation

# US-2: Find anagrams in a candidate list
def test_find_anagrams_returns_correct_matches():
    assert find_anagrams("listen", ["silent", "tinsel"]) == ["silent", "tinsel"]  # both are anagrams
    assert find_anagrams("listen", ["tinsel", "silent"]) == ["tinsel", "silent"]  # preserving candidate order

def test_find_anagrams_no_matches():
    assert find_anagrams("hello", ["world", "python"]) == []  # no matches

def test_find_anagrams_filters_non_anagrams():
    assert find_anagrams("master", ["stream", "maters", "pigeon"]) == ["stream", "maters"]  # keeping only anagrams

def test_find_anagrams_not_itself():
    assert find_anagrams("listen", ["listen", "silent"]) == ["silent"]  # ignoring identical word

def test_find_anagrams_case_space_punctuation_normalization():
    assert find_anagrams("Dormitory", ["Dirty Room", "DIRTY ROOM!", "DORMITORY"]) == ["Dirty Room", "DIRTY ROOM!"]  # normalizing

# US-3: Group a word list into anagram clusters
def test_group_anagrams_clusters_anagrams():
    assert group_anagrams(["eat", "tea", "ate"]) == [["eat", "tea", "ate"]]  # cluster of anagrams

def test_group_anagrams_single_word_clusters():
    assert group_anagrams(["hello", "world"]) == [["hello"], ["world"]]  # each forms own cluster

def test_group_anagrams_empty_list():
    assert group_anagrams([]) == []  # no clusters from empty list

def test_group_anagrams_ordered_by_first_appearance():
    assert group_anagrams(["bat", "tab", "cat"]) == [["bat", "tab"], ["cat"]]  # clusters ordered by first appearance

def test_group_anagrams_ordered_within_cluster():
    assert group_anagrams(["eat", "ate", "tea", "tan", "nat"]) == [["eat", "ate", "tea"], ["tan", "nat"]]  # order preserved

def test_group_anagrams_case_space_punctuation_normalization():
    assert group_anagrams(["Dormitory", "Dirty Room", "Moon starer!"]) == [["Dormitory", "Dirty Room"], ["Moon starer!"]]  # normalization applied