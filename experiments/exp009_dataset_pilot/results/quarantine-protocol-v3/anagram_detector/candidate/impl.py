# candidate/impl.py

import string

class AnagramTool:
    @staticmethod
    def normalize(text):
        """ Normalize the text by removing punctuation, spaces and converting to lower case. """
        return ''.join(char.lower() for char in text if char.isalnum())

    @staticmethod
    def are_anagrams(text1, text2):
        """ Check if two texts are anagrams of each other. """
        normalized1 = AnagramTool.normalize(text1)
        normalized2 = AnagramTool.normalize(text2)
        if normalized1 == normalized2:  # AC-1.4
            return False
        return sorted(normalized1) == sorted(normalized2)  # AC-1.1 and AC-1.2

    @staticmethod
    def find_anagrams(subject, candidates):
        """ Find all anagrams of the subject in the candidates list. """
        return [candidate for candidate in candidates 
                if AnagramTool.are_anagrams(subject, candidate) and candidate != subject]  # AC-2.4

    @staticmethod
    def group_anagrams(words):
        """ Group a list of words into anagram clusters. """
        anagram_map = {}
        for word in words:
            normalized = AnagramTool.normalize(word)
            sorted_word = ''.join(sorted(normalized))
            if sorted_word not in anagram_map:
                anagram_map[sorted_word] = []
            anagram_map[sorted_word].append(word)

        return [cluster for cluster in anagram_map.values() if len(cluster) > 1 or (len(cluster) == 1 and cluster[0] not in anagram_map)]  # AC-3.1, AC-3.2
