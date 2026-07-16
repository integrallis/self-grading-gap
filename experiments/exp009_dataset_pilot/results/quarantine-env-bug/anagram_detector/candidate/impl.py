# candidate/impl.py

import string

class AnagramDetector:
    @staticmethod
    def clean_text(text):
        """Cleans the text by removing spaces and punctuation, and converting to lowercase."""
        return ''.join(char.lower() for char in text if char.isalnum())

    @staticmethod
    def are_anagrams(text1, text2):
        """Determines if two texts are anagrams."""
        cleaned_text1 = AnagramDetector.clean_text(text1)
        cleaned_text2 = AnagramDetector.clean_text(text2)
        
        if cleaned_text1 == cleaned_text2:
            return False
        return sorted(cleaned_text1) == sorted(cleaned_text2)

    @staticmethod
    def find_anagrams(subject, candidates):
        """Finds all anagrams of the subject in the candidate list."""
        return [candidate for candidate in candidates if AnagramDetector.are_anagrams(subject, candidate)]

    @staticmethod
    def group_anagrams(words):
        """Groups words into clusters of anagrams."""
        anagram_map = {}
        for word in words:
            cleaned_word = AnagramDetector.clean_text(word)
            sorted_word = ''.join(sorted(cleaned_word))
            if sorted_word not in anagram_map:
                anagram_map[sorted_word] = []
            anagram_map[sorted_word].append(word)

        return [group for group in anagram_map.values() if len(group) > 1] + \
               [[word] for word in words if AnagramDetector.clean_text(word) not in anagram_map]

# Example usage:
if __name__ == "__main__":
    detector = AnagramDetector()
    print(detector.are_anagrams("listen", "silent"))  # True
    print(detector.find_anagrams("master", ["stream", "maters", "pigeon"]))  # ['stream', 'maters']
    print(detector.group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))  # [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
