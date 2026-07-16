# test_solution.py

from solution import detect_anagram, find_anagrams, group_anagram_clusters

def test_detect_anagram_positive_cases():
    assert detect_anagram("listen", "silent")  # Both contain: l, i, s, t, e, n
    assert detect_anagram("cat", "tac")        # Both contain: c, a, t
    assert detect_anagram("ab", "ba")          # Both contain: a, b
    assert detect_anagram("Dormitory", "Dirty Room")  # Ignore spaces; both contain: d, o, r, i, t, m, y
    assert detect_anagram("Astronomer", "Moon starer!")  # Ignore punctuation; both contain: a, e, m, n, o, r, s, t

def test_detect_anagram_negative_cases():
    assert not detect_anagram("hello", "world")  # Different letters
    assert not detect_anagram("aab", "abb")      # Different frequencies
    assert not detect_anagram("master", "stream")  # Same letters, but "master" is not an anagram of itself
    assert not detect_anagram("Cat", "cat")      # Same word differing only in case
    assert not detect_anagram("", "")             # Both are empty texts

def test_find_anagrams_positive_cases():
    assert find_anagrams("listen", ["silent", "tinsel"]) == ["silent", "tinsel"]  # Both are anagrams
    assert find_anagrams("master", ["stream", "maters"]) == ["stream", "maters"]  # Both are anagrams

def test_find_anagrams_negative_cases():
    assert find_anagrams("master", ["pigeon"]) == []  # No matches
    assert find_anagrams("listen", ["silent", "listen", "tinsel"]) == ["silent", "tinsel"]  # "listen" is not counted

def test_group_anagram_clusters():
    assert group_anagram_clusters(["eat", "tea", "ate"]) == [["eat", "tea", "ate"]]  # All are anagrams
    assert group_anagram_clusters(["eat", "tea", "bat"]) == [["eat", "tea"], ["bat"]]  # "bat" is separate
    assert group_anagram_clusters(["cat", "act", "dog", "god"]) == [["cat", "act"], ["dog", "god"]]  # Separate clusters
    assert group_anagram_clusters(["apple", "banana"]) == [["apple"], ["banana"]]  # No anagrams
    assert group_anagram_clusters([]) == []  # Empty list should yield no clusters