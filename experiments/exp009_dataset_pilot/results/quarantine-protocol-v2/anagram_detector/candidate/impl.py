import re
from collections import defaultdict

class AnagramTool:
    @staticmethod
    def clean_text(text):
        """Remove spaces and punctuation, convert to lowercase."""
        return re.sub(r'[\W_]+', '', text.lower())

    @staticmethod
    def are_anagrams(text1, text2):
        """Determine if two texts are anagrams."""
        cleaned1 = AnagramTool.clean_text(text1)
        cleaned2 = AnagramTool.clean_text(text2)
        
        if cleaned1 == cleaned2:
            return False
        return sorted(cleaned1) == sorted(cleaned2)

    @staticmethod
    def find_anagrams(subject, candidates):
        """Find all anagrams of the subject in the candidates list."""
        return [candidate for candidate in candidates 
                if AnagramTool.are_anagrams(subject, candidate)]

    @staticmethod
    def group_anagrams(word_list):
        """Group words into anagram clusters."""
        anagram_map = defaultdict(list)
        
        for word in word_list:
            cleaned_word = AnagramTool.clean_text(word)
            anagram_map[tuple(sorted(cleaned_word))].append(word)
        
        return [cluster for cluster in anagram_map.values() if len(cluster) > 1] + \
               [[word] for word in word_list if word not in anagram_map]

# Example usage
if __name__ == "__main__":
    tool = AnagramTool()
    print(tool.are_anagrams("listen", "silent"))  # True
    print(tool.find_anagrams("listen", ["silent", "tinsel", "enlist"]))  # ['silent', 'tinsel', 'enlist']
    print(tool.group_anagrams(["eat", "tea", "ate", "bat", "tab", "cat"]))  # [['eat', 'tea', 'ate'], ['bat', 'tab'], ['cat']]
