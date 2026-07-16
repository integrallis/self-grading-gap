def detect_anagram(word1, word2):
    if word1.lower() == word2.lower():
        return False
    import re
    cleaned_word1 = ''.join(sorted(re.sub(r'\W', '', word1.replace(' ', '').lower())))
    cleaned_word2 = ''.join(sorted(re.sub(r'\W', '', word2.replace(' ', '').lower())))
    return cleaned_word1 == cleaned_word2

def find_anagrams(word, candidates):
    return [candidate for candidate in candidates if detect_anagram(word, candidate)]

from collections import defaultdict

def group_anagram_clusters(words):
    anagram_map = defaultdict(list)
    for word in words:
        key = ''.join(sorted(word.lower().replace(' ', '').replace(r'\W', '')))
        anagram_map[key].append(word)
    return [group for group in anagram_map.values() if len(group) > 0]