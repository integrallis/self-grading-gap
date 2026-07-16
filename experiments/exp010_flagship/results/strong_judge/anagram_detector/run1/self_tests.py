# test_solution.py

from solution import are_anagrams, find_anagrams, group_anagram_clusters

def test_are_anagrams_identical_words_case_insensitive():
    assert not are_anagrams("listen", "listen")  # identical words

def test_are_anagrams_identical_words_different_case():
    assert not are_anagrams("Listen", "listen")  # same word differing only in case

def test_are_anagrams_identical_single_letters():
    assert not are_anagrams("a", "a")  # identical single letters

def test_are_anagrams_two_empty_texts():
    assert not are_anagrams("", "")  # two empty texts

def test_are_anagrams_anagrams():
    assert are_anagrams("listen", "silent")  # same letters with equal frequencies
    assert are_anagrams("cat", "tac")  # same letters with equal frequencies
    assert are_anagrams("ab", "ba")  # same letters with equal frequencies
    assert are_anagrams("Cat", "tac")  # case-insensitive match

def test_are_anagrams_not_anagrams_different_letters():
    assert not are_anagrams("hello", "world")  # different letters
    assert not are_anagrams("aab", "abb")  # different letter frequencies

def test_are_anagrams_spaces_ignored():
    assert are_anagrams("Dormitory", "Dirty Room")  # spaces ignored

def test_are_anagrams_punctuation_ignored():
    assert are_anagrams("Astronomer", "Moon starer!")  # punctuation ignored

def test_find_anagrams_in_candidate_list():
    assert list(find_anagrams("listen", ["silent", "tinsel", "enlist"])) == ["silent", "tinsel", "enlist"]  # all anagrams
    assert list(find_anagrams("master", ["stream", "maters", "pigeon"])) == ["stream", "maters"]  # filtered non-anagrams
    assert list(find_anagrams("listen", ["listen", "silent"])) == ["silent"]  # identical candidate not included
    assert list(find_anagrams("abc", ["def", "ghi"])) == []  # no matches
    assert list(find_anagrams("cat", ["tac", "Cat", "act"])) == ["tac", "Cat", "act"]  # case-insensitive matches

def test_group_anagram_clusters():
    assert [list(cluster) for cluster in group_anagram_clusters(["eat", "tea", "ate"])] == [["eat", "tea", "ate"]]  # single cluster
    assert [list(cluster) for cluster in group_anagram_clusters(["eat", "tea", "ate", "bat"])] == [["eat", "tea", "ate"], ["bat"]]  # one cluster and one single-word cluster
    assert group_anagram_clusters([]) == []  # empty word list
    assert [list(cluster) for cluster in group_anagram_clusters(["rat", "tar", "art", "hello"])] == [["rat", "tar", "art"], ["hello"]]  # mixed clusters
    assert [list(cluster) for cluster in group_anagram_clusters(["a", "A"])] == [["a"], ["A"]]  # case difference yields separate clusters
    assert [list(cluster) for cluster in group_anagram_clusters(["Dormitory", "Dirty Room"])] == [["Dormitory", "Dirty Room"]]  # case/space normalized clustering