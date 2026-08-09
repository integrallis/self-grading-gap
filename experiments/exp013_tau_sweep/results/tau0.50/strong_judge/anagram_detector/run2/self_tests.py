# test_solution.py

from solution import detect_anagram, find_anagrams, group_anagrams

# Test US-1: Detect whether two texts are anagrams
def test_anagrams_different_words():
    assert detect_anagram("listen", "silent")  # Same letters, different order
    assert detect_anagram("cat", "tac")  # Same letters, different order
    assert detect_anagram("ab", "ba")  # Same letters, different order

def test_anagrams_different_frequencies():
    assert not detect_anagram("hello", "world")  # Different letters
    assert not detect_anagram("aab", "abb")  # Different frequencies of 'a' and 'b'

def test_anagrams_case_insensitivity():
    assert detect_anagram("Cat", "tac")  # Same letters, different case

def test_anagrams_self_reference():
    assert not detect_anagram("word", "word")  # Identical words
    assert not detect_anagram("A", "a")  # Same letter, different case
    assert not detect_anagram("", "")  # Two empty texts
    assert not detect_anagram("a", "a")  # Identical single letters
    assert not detect_anagram("Word", "word")  # Same multi-letter word differing only in case

def test_anagrams_ignore_spaces():
    assert detect_anagram("Dormitory", "Dirty Room")  # Ignore spaces

def test_anagrams_ignore_punctuation():
    assert detect_anagram("Astronomer", "Moon starer!")  # Ignore punctuation

# Test US-2: Find anagrams in a candidate list
def test_find_anagrams_preserve_order():
    result = find_anagrams("listen", ["silent", "tinsel", "enlist"])
    assert result == ["silent", "tinsel", "enlist"]  # All are anagrams of "listen"

def test_find_anagrams_no_match():
    result = find_anagrams("listen", ["hello", "world"])
    assert result == []  # No matches

def test_find_anagrams_filter_non_anagrams():
    result = find_anagrams("master", ["stream", "maters", "pigeon"])
    assert result == ["stream", "maters"]  # Filtered out "pigeon"

def test_find_anagrams_identical_word_not_match():
    result = find_anagrams("listen", ["listen", "silent"])
    assert result == ["silent"]  # "listen" should not be included

def test_find_anagrams_case_only_excluded():
    result = find_anagrams("listen", ["Listen"])
    assert result == []  # "Listen" is the same as "listen" in a case-insensitive comparison

def test_find_anagrams_normalization_applies():
    result = find_anagrams("listen", ["Silent", " tinsel ", "enlist", "listen"])
    assert result == ["Silent", " tinsel ", "enlist"]  # Normalized candidates

def test_find_anagrams_punctuation_normalization():
    result = find_anagrams("Astronomer", ["Moon starer!"])
    assert result == ["Moon starer!"]  # Punctuation normalized

# Test US-3: Group a word list into anagram clusters
def test_group_anagrams_clusters():
    result = group_anagrams(["eat", "tea", "ate", "bat", "tab"])
    assert result == [["eat", "tea", "ate"], ["bat", "tab"]]  # Grouped correctly

def test_group_anagrams_unrelated_words():
    result = group_anagrams(["cat", "dog", "fish"])
    assert result == [["cat"], ["dog"], ["fish"]]  # Each forms its own cluster

def test_group_anagrams_empty_list():
    result = group_anagrams([])
    assert result == []  # No clusters from an empty list

def test_group_anagrams_order_of_clusters():
    result = group_anagrams(["eat", "bat", "tea", "tab", "ate"])
    assert result == [["eat", "tea", "ate"], ["bat", "tab"]]  # Clusters ordered by first appearance

def test_group_anagrams_order_with_identical_words():
    result = group_anagrams(["cat", "act", "dog", "god"])
    assert result == [["cat", "act"], ["dog", "god"]]  # Clusters with input order preserved

def test_group_anagrams_normalization():
    result = group_anagrams(["Dusty", "Study", "dusty", "st udy"])
    assert result == [["Dusty", "Study"], ["dusty", "st udy"]]  # Variations are not grouped

def test_group_anagrams_with_punctuation():
    result = group_anagrams(["Dusty!", "Study", "dusty", "st udy!"])
    assert result == [["Dusty!", "st udy!"], ["Study"], ["dusty"]]  # Punctuation considered