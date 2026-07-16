import string

class AnagramTool:
    @staticmethod
    def clean_text(text):
        """Remove spaces and punctuation, and convert to lower case."""
        return ''.join(char.lower() for char in text if char.isalnum())

    @staticmethod
    def are_anagrams(text1, text2):
        """Check if two texts are anagrams of each other."""
        cleaned_text1 = AnagramTool.clean_text(text1)
        cleaned_text2 = AnagramTool.clean_text(text2)

        if cleaned_text1 == cleaned_text2:
            return False  # Not an anagram if texts are identical after cleaning

        return sorted(cleaned_text1) == sorted(cleaned_text2)

    @staticmethod
    def find_anagrams(subject, candidates):
        """Find all anagrams of the subject word in a candidate list."""
        subject_cleaned = AnagramTool.clean_text(subject)
        return [candidate for candidate in candidates if 
                AnagramTool.are_anagrams(subject, candidate) and 
                AnagramTool.clean_text(candidate) != subject_cleaned]

    @staticmethod
    def group_anagrams(words):
        """Group words into clusters of anagrams."""
        anagram_dict = {}
        for word in words:
            cleaned_word = AnagramTool.clean_text(word)
            sorted_word = ''.join(sorted(cleaned_word))
            if sorted_word in anagram_dict:
                anagram_dict[sorted_word].append(word)
            else:
                anagram_dict[sorted_word] = [word]

        return [cluster for cluster in anagram_dict.values() if len(cluster) > 1 or len(cluster) == 1]

# Example usage (not part of the module):
if __name__ == "__main__":
    tool = AnagramTool()
    print(tool.are_anagrams("listen", "silent"))  # True
    print(tool.find_anagrams("listen", ["silent", "tinsel", "enlist", "google"]))  # ['silent', 'tinsel', 'enlist']
    print(tool.group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))  # [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
