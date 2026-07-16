def are_anagrams(str1: str, str2: str) -> bool:
    import string
    # Normalize the strings: lower case, remove spaces and punctuation
    str1_cleaned = ''.join(filter(str.isalnum, str1.lower()))
    str2_cleaned = ''.join(filter(str.isalnum, str2.lower()))
    # Anagrams must not be identical and must have the same sorted letters
    return str1_cleaned != str2_cleaned and sorted(str1_cleaned) == sorted(str2_cleaned)


def find_anagrams(word: str, candidates: list) -> list:
    candidates = [candidate for candidate in candidates if candidate != word and are_anagrams(word, candidate)]
    return candidates


def group_anagram_clusters(words: list) -> list:
    from collections import defaultdict
    anagrams = defaultdict(list)
    for word in words:
        key = ''.join(sorted(word))
        anagrams[key].append(word)
    return [group for group in anagrams.values()]