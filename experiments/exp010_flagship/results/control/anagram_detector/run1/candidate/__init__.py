def detect_anagram(str1, str2):
    # Normalize both strings by removing spaces and punctuation, and converting to lowercase
    str1 = ''.join(filter(str.isalnum, str1)).lower()
    str2 = ''.join(filter(str.isalnum, str2)).lower()
    if str1 == str2:
        return False
    return sorted(str1) == sorted(str2)

def find_anagrams(word, candidates):
    return [candidate for candidate in candidates if detect_anagram(word, candidate) and candidate != word]

def group_anagram_clusters(words):
    from collections import defaultdict
    anagram_map = defaultdict(list)
    for word in words:
        key = ''.join(sorted(word.lower()))  # Sort letters of the word to create a key
        anagram_map[key].append(word)
    return list(anagram_map.values())