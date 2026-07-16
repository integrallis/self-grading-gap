# your complete test file
import pytest
from solution import are_anagrams, find_anagrams, group_anagram_clusters

# US-1: Detect whether two texts are anagrams

def test_anagrams_different_words():
    assert are_anagrams("listen", "silent")  # 'listen' and 'silent' are anagrams
    assert are_anagrams("cat", "tac")        # 'cat' and 'tac' are anagrams
    assert are_anagrams("ab", "ba")          # 'ab' and 'ba' are anagrams

def test_anagrams_not_anagrams():
    assert not are_anagrams("hello", "world")  # Different letters
    assert not are_anagrams("aab", "abb")      # Different frequencies of letters

def test_anagrams_case_insensitive():
    assert are_anagrams("Cat", "tac")          # Case-insensitive match

def test_anagrams_not_itself():
    assert not are_anagrams("word", "word")    # Identical words
    assert not are_anagrams("A", "a")          # Same letter, different case
    assert not are_anagrams("", "")             # Two empty texts

def test_anagrams_ignore_spaces():
    assert are_anagrams("Dormitory", "Dirty Room")  # Ignore spaces

def test_anagrams_ignore_punctuation():
    assert are_anagrams("Astronomer", "Moon starer!")  # Ignore punctuation

# US-2: Find anagrams in a candidate list

def test_find_anagrams_returns_correct_candidates():
    assert find_anagrams("listen", ["silent", "tinsel"]) == ["silent", "tinsel"]  # Both are anagrams of 'listen'

def test_find_anagrams_no_matches():
    assert find_anagrams("listen", ["hello", "world"]) == []  # No anagrams found

def test_find_anagrams_filters_non_anagrams():
    assert find_anagrams("master", ["stream", "maters", "pigeon"]) == ["stream", "maters"]  # 'pigeon' is not an anagram

def test_find_anagrams_excludes_identical_candidate():
    assert find_anagrams("listen", ["listen", "silent"]) == ["silent"]  # Excludes 'listen' itself

# US-3: Group a word list into anagram clusters

def test_group_anagram_clusters():
    assert group_anagram_clusters(["eat", "tea", "ate"]) == [["eat", "tea", "ate"]]  # All form a single cluster

def test_group_anagram_clusters_unrelated_words():
    assert group_anagram_clusters(["eat", "hello"]) == [["eat"], ["hello"]]  # Unrelated words each form their own cluster

def test_group_anagram_clusters_empty_list():
    assert group_anagram_clusters([]) == []  # Empty list yields no clusters

def test_group_anagram_clusters_order_preserved():
    assert group_anagram_clusters(["bat", "tab", "cat"]) == [["bat", "tab"], ["cat"]]  # Clusters ordered by first appearance