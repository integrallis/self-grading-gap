# test_solution.py

from solution import detect_anagram, find_anagrams, group_anagrams

def test_detect_anagram_different_anagrams():
    assert detect_anagram("listen", "silent")  # "listen" and "silent" are anagrams
    assert detect_anagram("cat", "tac")  # "cat" and "tac" are anagrams
    assert detect_anagram("ab", "ba")  # "ab" and "ba" are anagrams

def test_detect_anagram_not_anagrams():
    assert not detect_anagram("hello", "world")  # Different letters
    assert not detect_anagram("aab", "abb")  # Different frequencies of letters

def test_detect_anagram_case_insensitivity():
    assert detect_anagram("Cat", "tac")  # Same letters, different case

def test_detect_anagram_self_match():
    assert not detect_anagram("word", "word")  # Same word
    assert not detect_anagram("A", "A")  # Same single letter
    assert not detect_anagram("word", "WORD")  # Same word, different case
    assert not detect_anagram("", "")  # Both empty

def test_detect_anagram_ignore_spaces():
    assert detect_anagram("Dormitory", "Dirty Room")  # Ignore spaces

def test_detect_anagram_ignore_punctuation():
    assert detect_anagram("Astronomer", "Moon starer!")  # Ignore punctuation

def test_find_anagrams_with_matches():
    candidates = ["silent", "tinsel", "enlist", "hello"]
    assert list(find_anagrams("listen", candidates)) == ["silent", "tinsel", "enlist"]  # Return anagrams

def test_find_anagrams_no_matches():
    candidates = ["hello", "world"]
    assert list(find_anagrams("listen", candidates)) == []  # No anagrams found

def test_find_anagrams_ignore_self_word():
    candidates = ["listen", "silent", "listen"]
    assert list(find_anagrams("listen", candidates)) == ["silent"]  # "listen" is ignored

def test_find_anagrams_case_insensitivity():
    candidates = ["tac", "ACT", "cat", "CAT"]
    assert list(find_anagrams("Cat", candidates)) == ["tac", "ACT"]  # Case insensitive matches

def test_find_anagrams_ignore_spaces():
    candidates = ["Dirty Room", "dorm room"]
    assert list(find_anagrams("Dormitory", candidates)) == ["Dirty Room"]  # Ignore spaces

def test_find_anagrams_ignore_punctuation():
    candidates = ["Moon starer!", "moon-starer"]
    assert list(find_anagrams("Astronomer", candidates)) == ["Moon starer!", "moon-starer"]  # Ignore punctuation

def test_group_anagrams_with_clusters():
    words = ["eat", "tea", "ate", "bat"]
    assert [list(c) for c in group_anagrams(words)] == [["eat", "tea", "ate"], ["bat"]]  # Clusters of anagrams

def test_group_anagrams_unrelated_words():
    words = ["cat", "dog", "fish"]
    assert [list(c) for c in group_anagrams(words)] == [["cat"], ["dog"], ["fish"]]  # Each word forms its own cluster

def test_group_anagrams_empty_list():
    words = []
    assert list(group_anagrams(words)) == []  # No clusters from an empty list

def test_group_anagrams_order_of_clusters():
    words = ["tea", "eat", "bat", "tab"]
    assert [list(c) for c in group_anagrams(words)] == [["tea", "eat"], ["bat", "tab"]]  # Clusters maintain input order

def test_group_anagrams_case_insensitivity():
    words = ["Cat", "tac", "dog"]
    assert [list(c) for c in group_anagrams(words)] == [["Cat", "tac"], ["dog"]]  # Case insensitive grouping

def test_group_anagrams_ignore_spaces():
    words = ["Dormitory", "Dirty Room", "cat"]
    assert [list(c) for c in group_anagrams(words)] == [["Dormitory", "Dirty Room"], ["cat"]]  # Ignore spaces

def test_group_anagrams_ignore_punctuation():
    words = ["Astronomer", "Moon starer!", "cat"]
    assert [list(c) for c in group_anagrams(words)] == [["Astronomer", "Moon starer!"], ["cat"]]  # Ignore punctuation

def test_group_anagrams_self_anagram_exclusion():
    words = ["eat", "eat", "Eat"]
    assert [list(c) for c in group_anagrams(words)] == [["eat"], ["eat"], ["Eat"]]  # Self-anagrams are excluded