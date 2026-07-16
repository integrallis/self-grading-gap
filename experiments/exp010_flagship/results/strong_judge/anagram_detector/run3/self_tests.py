from solution import detect_anagram, find_anagrams, group_anagrams

def test_detect_anagram_different_anagrams():
    assert detect_anagram("listen", "silent")  # "listen" and "silent" are anagrams
    assert detect_anagram("cat", "tac")  # "cat" and "tac" are anagrams
    assert detect_anagram("ab", "ba")  # "ab" and "ba" are anagrams

def test_detect_anagram_not_anagrams():
    assert not detect_anagram("hello", "world")  # "hello" and "world" are not anagrams
    assert not detect_anagram("aab", "abb")  # "aab" and "abb" are not anagrams

def test_detect_anagram_case_insensitivity():
    assert detect_anagram("Cat", "tac")  # "Cat" and "tac" are anagrams (case insensitive)

def test_detect_anagram_self_anagram():
    assert not detect_anagram("listen", "listen")  # identical words are not anagrams
    assert not detect_anagram("A", "A")  # identical single letters are not anagrams
    assert not detect_anagram("word", "WORD")  # same word differing only in case is not anagram
    assert not detect_anagram("", "")  # two empty texts are not anagrams

def test_detect_anagram_ignore_spaces():
    assert detect_anagram("Dormitory", "Dirty Room")  # spaces ignored

def test_detect_anagram_ignore_punctuation():
    assert detect_anagram("Astronomer", "Moon starer!")  # punctuation ignored

def test_find_anagrams_with_matches():
    assert find_anagrams("listen", ["silent", "tinsel"]) == ["silent", "tinsel"]  # both are anagrams

def test_find_anagrams_no_matches():
    assert find_anagrams("listen", ["hello", "world"]) == []  # no matches

def test_find_anagrams_filter_non_anagrams():
    assert find_anagrams("master", ["stream", "maters", "pigeon"]) == ["stream", "maters"]  # only valid anagrams

def test_find_anagrams_ignore_self():
    assert find_anagrams("listen", ["listen", "silent"]) == ["silent"]  # "listen" is not counted

def test_find_anagrams_case_insensitivity():
    assert find_anagrams("Cat", ["cat", "tac"]) == ["tac"]  # "Cat" and "tac" are anagrams, "cat" is excluded

def test_find_anagrams_ignore_spaces():
    assert find_anagrams("Dormitory", ["Dirty Room", "ordinary"]) == ["Dirty Room"]  # spaces ignored

def test_find_anagrams_ignore_punctuation():
    assert find_anagrams("Astronomer", ["Moon starer!", "moon"]) == ["Moon starer!"]  # punctuation ignored

def test_group_anagrams_multiple_clusters():
    assert group_anagrams(["eat", "tea", "ate", "bat", "tab"]) == [["eat", "tea", "ate"], ["bat", "tab"]]  # clusters formed

def test_group_anagrams_single_word_clusters():
    assert group_anagrams(["hello", "world"]) == [["hello"], ["world"]]  # unrelated words form single clusters

def test_group_anagrams_empty_list():
    assert group_anagrams([]) == []  # empty list yields no clusters

def test_group_anagrams_ordered_by_first_appearance():
    assert group_anagrams(["bat", "tab", "eat", "tea", "ate"]) == [["bat", "tab"], ["eat", "tea", "ate"]]  # ordered by first appearance

def test_group_anagrams_keep_input_order_in_clusters():
    assert group_anagrams(["eat", "ate", "tea", "bat", "tab"]) == [["eat", "ate", "tea"], ["bat", "tab"]]  # maintain input order within clusters

def test_group_anagrams_case_insensitivity():
    assert group_anagrams(["Cat", "tac", "dog"]) == [["Cat"], ["cat", "tac"], ["dog"]]  # "Cat" and "tac" are not clustered together

def test_group_anagrams_ignore_spaces():
    assert group_anagrams(["Dormitory", "Dirty Room", "cat"]) == [["Dormitory", "Dirty Room"], ["cat"]]  # spaces ignored

def test_group_anagrams_ignore_punctuation():
    assert group_anagrams(["Astronomer", "Moon starer!", "cat"]) == [["Astronomer", "Moon starer!"], ["cat"]]  # punctuation ignored