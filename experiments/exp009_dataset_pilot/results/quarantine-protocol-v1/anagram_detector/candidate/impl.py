# candidate/impl.py

import string

class AnagramUtility:
    @staticmethod
    def normalize(text):
        # Remove punctuation and spaces, and convert to lowercase
        return ''.join(char.lower() for char in text if char.isalnum())

    @staticmethod
    def are_anagrams(text1, text2):
        # Check if two texts are anagrams
        if text1 == text2:
            return False
        normalized1 = AnagramUtility.normalize(text1)
        normalized2 = AnagramUtility.normalize(text2)
        return sorted(normalized1) == sorted(normalized2)

    @staticmethod
    def find_anagrams(subject, candidates):
        # Find all anagrams of the subject in the candidate list
        return [candidate for candidate in candidates if AnagramUtility.are_anagrams(subject, candidate) and candidate != subject]

    @staticmethod
    def group_anagrams(words):
        # Group words into anagram clusters
        anagram_map = {}
        for word in words:
            normalized = AnagramUtility.normalize(word)
            sorted_word = ''.join(sorted(normalized))
            if sorted_word not in anagram_map:
                anagram_map[sorted_word] = []
            anagram_map[sorted_word].append(word)
        
        # Filter out single-word clusters and return clusters maintaining input order
        return [cluster for cluster in anagram_map.values() if len(cluster) > 1] + \
               [word for word in words if word not in anagram_map or len(anagram_map[AnagramUtility.normalize(word)]) == 1]
