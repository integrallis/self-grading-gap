# test_solution.py

from solution import detect_anagram, find_anagrams_in_list, group_anagrams

def test_detect_anagram_different_anagrams():
    assert detect_anagram("listen", "silent")  # "listen" and "silent" are anagrams
    assert detect_anagram("cat", "tac")  # "cat" and "tac" are anagrams
    assert detect_anagram("ab", "ba")  # "ab" and "ba" are anagrams

def test_detect_anagram_not_anagrams():
    assert not detect_anagram("hello", "world")  # Different letters
    assert not detect_anagram("aab", "abb")  # Different letter frequencies

def test_detect_anagram_case_insensitivity():
    assert detect_anagram("Cat", "tac")  # Case insensitive anagrams

def test_detect_anagram_self_anagram():
    assert not detect_anagram("word", "word")  # Identical words
    assert not detect_anagram("A", "a")  # Same letter, different case
    assert not detect_anagram("", "")  # Both are empty texts

def test_detect_anagram_ignore_spaces():
    assert detect_anagram("Dormitory", "Dirty Room")  # Spaces ignored

def test_detect_anagram_ignore_punctuation():
    assert detect_anagram("Astronomer", "Moon starer!")  # Punctuation ignored

def test_detect_anagram_identical_single_letters():
    assert not detect_anagram("a", "a")  # Identical single letters rejected

def test_find_anagrams_in_list_matches_found():
    assert find_anagrams_in_list("listen", ["silent", "tinsel"]) == ["silent", "tinsel"]  # Both are anagrams

def test_find_anagrams_in_list_no_matches():
    assert find_anagrams_in_list("listen", ["hello", "world"]) == []  # No anagrams found

def test_find_anagrams_in_list_candidates_filtered():
    assert find_anagrams_in_list("master", ["stream", "maters", "pigeon"]) == ["stream", "maters"]  # Non-anagrams dropped

def test_find_anagrams_in_list_self_candidate():
    assert find_anagrams_in_list("listen", ["listen", "silent"]) == ["silent"]  # "listen" is not counted

def test_find_anagrams_in_list_case_insensitivity():
    assert find_anagrams_in_list("Listen", ["silent", "tinsel"]) == ["silent", "tinsel"]  # Case insensitive matching

def test_find_anagrams_in_list_frequency_filter():
    assert find_anagrams_in_list("aab", ["abb"]) == []  # Different letter frequencies

def test_find_anagrams_in_list_ignore_spaces_and_punctuation():
    assert find_anagrams_in_list("Dormitory", ["Dirty Room", "moon starer!"]) == ["Dirty Room", "moon starer!"]  # Both match after normalization

def test_group_anagrams_clusters():
    assert group_anagrams(["eat", "tea", "ate"]) == [["eat", "tea", "ate"]]  # All form a single cluster

def test_group_anagrams_unrelated_words():
    assert group_anagrams(["hello", "world"]) == [["hello"], ["world"]]  # Each forms its own cluster

def test_group_anagrams_empty_list():
    assert group_anagrams([]) == []  # Empty input yields no clusters

def test_group_anagrams_ordered_clusters():
    assert group_anagrams(["eat", "hello", "tea", "ate", "world"]) == [["eat", "tea", "ate"], ["hello"], ["world"]]  # Clusters ordered by first appearance

def test_group_anagrams_case_insensitivity():
    assert group_anagrams(["Eat", "tea"]) == [["Eat", "tea"]]  # Case-insensitive clustering

def test_group_anagrams_ignore_spaces_and_punctuation():
    assert group_anagrams(["Dormitory", "Dirty Room", "moon starer!"]) == [["Dormitory", "Dirty Room"], ["moon starer!"]]  # Clusters ignore spaces and punctuation

def test_group_anagrams_frequency_separation():
    assert group_anagrams(["aab", "abb"]) == [["aab"], ["abb"]]  # Different frequencies remain separate clusters

def test_group_anagrams_duplicate_words():
    assert group_anagrams(["word", "word"]) == [["word"]]  # Identical words are not mutual anagrams