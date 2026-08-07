# test_solution.py

from solution import detect_anagram, find_anagrams, group_anagrams

def test_detect_anagram_valid_cases():
    # AC-1.1: "listen" and "silent" are anagrams
    assert detect_anagram("listen", "silent") is True
    # AC-1.1: "cat" and "tac" are anagrams
    assert detect_anagram("cat", "tac") is True
    # AC-1.1: "ab" and "ba" are anagrams
    assert detect_anagram("ab", "ba") is True
    # AC-1.3: "Cat" and "tac" are anagrams (case insensitive)
    assert detect_anagram("Cat", "tac") is True
    # AC-1.5: "Dormitory" and "Dirty Room" are anagrams (spaces ignored)
    assert detect_anagram("Dormitory", "Dirty Room") is True
    # AC-1.6: "Astronomer" and "Moon starer!" are anagrams (punctuation ignored)
    assert detect_anagram("Astronomer", "Moon starer!") is True

def test_detect_anagram_invalid_cases():
    # AC-1.2: "hello" and "world" are not anagrams
    assert detect_anagram("hello", "world") is False
    # AC-1.2: "aab" and "abb" are not anagrams
    assert detect_anagram("aab", "abb") is False
    # AC-1.4: "word" is not an anagram of itself
    assert detect_anagram("word", "word") is False
    # AC-1.4: "A" is not an anagram of itself
    assert detect_anagram("A", "A") is False
    # AC-1.4: Two empty texts are not anagrams
    assert detect_anagram("", "") is False
    # AC-1.4: "word" and "WORD" are not anagrams of themselves
    assert detect_anagram("word", "WORD") is False

def test_find_anagrams():
    # AC-2.1: "listen" finds anagrams "silent" and "tinsel"
    assert find_anagrams("listen", ["silent", "tinsel"]) == ["silent", "tinsel"]
    # AC-2.1: "Astronomer" finds anagrams "Moon starer!"
    assert find_anagrams("Astronomer", ["Moon starer!"]) == ["Moon starer!"]
    # AC-2.2: No candidates match
    assert find_anagrams("word", ["hello", "world"]) == []
    # AC-2.3: "master" keeps "stream" and "maters" but drops "pigeon"
    assert find_anagrams("master", ["stream", "maters", "pigeon"]) == ["stream", "maters"]
    # AC-2.4: "listen" does not match "listen"
    assert find_anagrams("listen", ["listen", "silent"]) == ["silent"]

def test_group_anagrams():
    # AC-3.1: "eat", "tea", "ate" cluster together
    assert group_anagrams(["eat", "tea", "ate"]) == [["eat", "tea", "ate"]]
    # AC-3.1: "Astronomer" and "Moon starer!" cluster together
    assert group_anagrams(["Astronomer", "Moon starer!", "cat"]) == [["Astronomer", "Moon starer!"], ["cat"]]
    # AC-3.2: "hello" and "world" are unrelated, form their own clusters
    assert group_anagrams(["hello", "world"]) == [["hello"], ["world"]]
    # AC-3.3: Empty list yields no clusters
    assert group_anagrams([]) == []
    # AC-3.4: Clusters ordered by first appearance, "eat", "tea", "ate" come before "bat", "tab"
    assert group_anagrams(["eat", "bat", "tea", "tab", "ate"]) == [["eat", "tea", "ate"], ["bat", "tab"]]