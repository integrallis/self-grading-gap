# test_solution.py

from solution import detect_anagram, find_anagrams, group_anagram_clusters

def test_detect_anagram_different_anagrams():
    # "listen" and "silent" are anagrams
    assert detect_anagram("listen", "silent") is True
    # "cat" and "tac" are anagrams
    assert detect_anagram("cat", "tac") is True
    # "ab" and "ba" are anagrams
    assert detect_anagram("ab", "ba") is True

def test_detect_anagram_not_anagrams():
    # "hello" and "world" are not anagrams
    assert detect_anagram("hello", "world") is False
    # "aab" and "abb" are not anagrams
    assert detect_anagram("aab", "abb") is False

def test_detect_anagram_case_insensitivity():
    # "Cat" and "tac" are anagrams (case insensitive)
    assert detect_anagram("Cat", "tac") is True

def test_detect_anagram_identical_texts():
    # "listen" and "listen" are not anagrams (identical)
    assert detect_anagram("listen", "listen") is False
    # "A" and "a" are not anagrams (identical)
    assert detect_anagram("A", "a") is False
    # Two empty texts are not anagrams
    assert detect_anagram("", "") is False

def test_detect_anagram_ignore_spaces():
    # "Dormitory" and "Dirty Room" are anagrams (spaces ignored)
    assert detect_anagram("Dormitory", "Dirty Room") is True

def test_detect_anagram_ignore_punctuation():
    # "Astronomer" and "Moon starer!" are anagrams (punctuation ignored)
    assert detect_anagram("Astronomer", "Moon starer!") is True

def test_find_anagrams():
    # "listen" should find "silent" and "tinsel" in the candidates
    assert find_anagrams("listen", ["silent", "tinsel", "enlist"]) == ["silent", "tinsel"]
    
def test_find_anagrams_no_matches():
    # "hello" should not find any matches in the candidates
    assert find_anagrams("hello", ["world", "python"]) == []

def test_find_anagrams_filter_non_anagrams():
    # "master" should find "stream" and "maters", but not "pigeon"
    assert find_anagrams("master", ["stream", "maters", "pigeon"]) == ["stream", "maters"]

def test_find_anagrams_ignore_identical_candidate():
    # "listen" should not find itself in the candidates
    assert find_anagrams("listen", ["listen", "silent"]) == ["silent"]

def test_group_anagram_clusters():
    # "eat", "tea", "ate" should cluster together
    assert group_anagram_clusters(["eat", "tea", "ate", "bat", "tab"]) == [["eat", "tea", "ate"], ["bat", "tab"]]

def test_group_anagram_clusters_single_words():
    # "dog" and "cat" should be their own clusters
    assert group_anagram_clusters(["dog", "cat"]) == [["dog"], ["cat"]]

def test_group_anagram_clusters_empty_list():
    # An empty word list should yield no clusters
    assert group_anagram_clusters([]) == []

def test_group_anagram_clusters_order_preserved():
    # Clusters should maintain the order of first appearance
    assert group_anagram_clusters(["bat", "tab", "eat", "tea", "ate"]) == [["bat", "tab"], ["eat", "tea", "ate"]]