# test_anagram_detection.py

from solution import detect_anagrams, find_anagrams_in_list, group_anagram_clusters

def test_detect_anagrams_different_anagrams():
    assert detect_anagrams("listen", "silent")  # 'listen' and 'silent' are anagrams
    assert detect_anagrams("cat", "tac")        # 'cat' and 'tac' are anagrams
    assert detect_anagrams("ab", "ba")          # 'ab' and 'ba' are anagrams

def test_detect_anagrams_not_anagrams():
    assert not detect_anagrams("hello", "world")  # 'hello' and 'world' are not anagrams
    assert not detect_anagrams("aab", "abb")      # 'aab' and 'abb' are not anagrams

def test_detect_anagrams_case_insensitivity():
    assert detect_anagrams("Cat", "tac")          # 'Cat' and 'tac' are anagrams case-insensitively

def test_detect_anagrams_identical_words():
    assert not detect_anagrams("word", "word")    # identical words are not anagrams
    assert not detect_anagrams("a", "a")          # identical single letters are not anagrams
    assert not detect_anagrams("TEST", "test")    # same word differing only in case is not anagram
    assert not detect_anagrams("", "")              # two empty texts are not anagrams

def test_detect_anagrams_ignore_spaces_and_punctuation():
    assert detect_anagrams("Dormitory", "Dirty Room")  # spaces are ignored
    assert detect_anagrams("Astronomer", "Moon starer!") # punctuation is ignored

def test_find_anagrams_in_list_found_anagrams():
    assert list(find_anagrams_in_list("listen", ["silent", "tinsel"])) == ["silent", "tinsel"]  # both are anagrams

def test_find_anagrams_in_list_no_matches():
    assert list(find_anagrams_in_list("listen", ["hello", "world"])) == []  # no anagrams found

def test_find_anagrams_in_list_filter_non_anagrams():
    assert list(find_anagrams_in_list("master", ["stream", "maters", "pigeon"])) == ["stream", "maters"]  # filtered out 'pigeon'

def test_find_anagrams_in_list_identical_word_not_found():
    assert list(find_anagrams_in_list("listen", ["listen"])) == []  # identical word is not an anagram

def test_find_anagrams_in_list_case_insensitivity():
    assert list(find_anagrams_in_list("Listen", ["listen", "silent"])) == ["silent"]  # case-only self-anagram exclusion

def test_find_anagrams_in_list_ignore_punctuation():
    assert list(find_anagrams_in_list("Astronomer", ["Moon starer!", "hello"])) == ["Moon starer!"]  # punctuation is ignored

def test_group_anagram_clusters_multiple_clusters():
    assert [list(cluster) for cluster in group_anagram_clusters(["eat", "tea", "ate", "bat", "tab"])] == [["eat", "tea", "ate"], ["bat", "tab"]]  # clusters formed

def test_group_anagram_clusters_single_words():
    assert [list(cluster) for cluster in group_anagram_clusters(["hello", "world"])] == [["hello"], ["world"]]  # unrelated words each form their own cluster

def test_group_anagram_clusters_empty_list():
    assert list(group_anagram_clusters([])) == []  # empty list yields no clusters

def test_group_anagram_clusters_order_preserved():
    assert [list(cluster) for cluster in group_anagram_clusters(["bat", "tab", "eat", "tea"])] == [["bat", "tab"], ["eat", "tea"]]  # order preserved

def test_group_anagram_clusters_case_insensitivity():
    assert [list(cluster) for cluster in group_anagram_clusters(["Dormitory", "dIrTy RoOm", "cat", "Tac!"])] == [["Dormitory", "dIrTy RoOm"], ["cat", "Tac!"]]  # clusters with case and punctuation ignored