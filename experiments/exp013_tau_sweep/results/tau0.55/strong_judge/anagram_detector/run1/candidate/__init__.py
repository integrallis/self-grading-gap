def normalize_string(s):
    return ''.join(sorted(ch.lower() for ch in s if ch.isalnum()))


def detect_anagram(word1, word2):
    clean_string = lambda s: ''.join(ch.lower() for ch in s if ch.isalnum())
    if clean_string(word1) == clean_string(word2):
        return False
    return normalize_string(word1) == normalize_string(word2)


def find_anagrams(word, candidates):
    return (candidate for candidate in candidates if detect_anagram(word, candidate))


def group_anagrams(words):
    anagrams_map = {}
    result = []
    for word in words:
        cleaned = ''.join(ch.lower() for ch in word if ch.isalnum())
        normalized = normalize_string(word)
        if normalized not in anagrams_map:
            anagrams_map[normalized] = []
        # Check if cleaned is already in the current anagram group
        if any(cleaned == ''.join(ch.lower() for ch in w if ch.isalnum()) for w in anagrams_map[normalized]):
            result.append([word])  # Add as new cluster
        else:
            anagrams_map[normalized].append(word)
    # Collect all clusters preserving order
    for cluster in anagrams_map.values():
        result.append(cluster)
    return result