from collections import defaultdict
import string

def normalize(text):
    # Normalize by removing punctuation, spaces and converting to lower case
    return ''.join(sorted(text.lower().translate(str.maketrans('', '', string.punctuation)).replace(' ', '')))

def detect_anagram(word1, word2):
    # Anagrams must be different words
    if word1.lower() == word2.lower():
        return False
    return normalize(word1) == normalize(word2)

def find_anagrams(word, candidates):
    normalized_word = normalize(word)
    return [candidate for candidate in candidates if normalize(candidate) == normalized_word and candidate.lower() != word.lower()]

def group_anagram_clusters(words):
    anagrams = defaultdict(list)
    for word in words:
        normalized = normalize(word)
        anagrams[normalized].append(word)
    return list(anagrams.values())