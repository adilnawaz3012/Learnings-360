from typing import List

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        # If list is empty, return "" string
        if not strs:
            return ""

        # Get the first string to compare with others
        first_str = strs[0]
        for idx in range(len(first_str)):
            # Loop though each char from reference string, i.e first_str
            curr_char = first_str[idx]
            # Start comparing with other string list
            for comp_str in strs[1:]:
                # if idx >= len(comp_str) means next string is smaller than current
                # if char doesn't match
                if idx >= len(comp_str) or comp_str[idx] != curr_char:
                    # return the substring which matched till now
                    return first_str[:idx]
        # If it doesn't returns, means everything matched, so return the reference string, i.e first_str
        return first_str