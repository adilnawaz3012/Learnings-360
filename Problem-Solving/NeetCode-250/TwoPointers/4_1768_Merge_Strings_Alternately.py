class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        i, j = 0, 0
        new_string = ""
        while i < len(word1) and j < len(word2):
            new_string += word1[i]
            new_string += word2[j]
            i += 1
            j += 1
        
        while i < len(word1):
            new_string += word1[i]
            i += 1

        while j < len(word2):
            new_string += word2[j]
            j += 1
        return new_string