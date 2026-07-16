# test_solution.py

from solution import detect_anagram, find_anagrams, group_anagram_clusters

def test_detect_anagram_different_words_anagram():
    assert detect_anagram("listen", "silent")  # both contain l, i, s, e, n
    assert detect_anagram("cat", "tac")  # both contain c, a, t
    assert detect_anagram("ab", "ba")  # both contain a, b

def test_detect_anagram_different_words_not_anagram():
    assert not detect_anagram("hello", "world")  # different letters
    assert not detect_anagram("aab", "abb")  # different frequencies of a and b

def test_detect_anagram_case_insensitivity():
    assert detect_anagram("Cat", "tac")  # both contain c, a, t

def test_detect_anagram_self_comparison():
    assert not detect_anagram("listen", "listen")  # identical words
    assert not detect_anagram("a", "a")  # identical single letters
    assert not detect_anagram("Hello", "hello")  # same word differing in case
    assert not detect_anagram("", "")  # two empty texts

def test_detect_anagram_ignore_spaces():
    assert detect_anagram("Dormitory", "Dirty Room")  # ignores spaces

def test_detect_anagram_ignore_punctuation():
    assert detect_anagram("Astronomer", "Moon starer!")  # ignores punctuation

def test_find_anagrams_matching_candidates():
    assert find_anagrams("listen", ["silent", "tinsel"]) == ["silent", "tinsel"]  # both are anagrams
    assert find_anagrams("master", ["stream", "maters"]) == ["stream", "maters"]  # both are anagrams

def test_find_anagrams_no_matches():
    assert find_anagrams("pigeon", ["stream", "maters"]) == []  # no matches

def test_find_anagrams_ignore_identical_word():
    assert find_anagrams("listen", ["silent", "listen"]) == ["silent"]  # "listen" is not counted

def test_group_anagram_clusters():
    assert group_anagram_clusters(["eat", "tea", "ate"]) == [["eat", "tea", "ate"]]  # cluster together

def test_group_anagram_clusters_unrelated_words():
    assert group_anagram_clusters(["eat", "dog", "god"]) == [["eat"], ["dog", "god"]]  # "dog" and "god" cluster

def test_group_anagram_clusters_empty_list():
    assert group_anagram_clusters([]) == []  # no clusters for empty list

def test_group_anagram_clusters_order_of_appearance():
    assert group_anagram_clusters(["eat", "tea", "dog", "god", "ate"]) == [["eat", "tea", "ate"], ["dog", "god"]]  # retains order