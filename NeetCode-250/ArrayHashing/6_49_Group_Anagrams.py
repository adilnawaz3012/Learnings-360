from typing import List

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        from collections import defaultdict
        hash_map = defaultdict(list)
        for _str in strs:
            sorted_str = "".join(sorted(_str))
            hash_map[sorted_str].append(_str)
        result = []
        for val in hash_map.values():
            result.append(val)
        return result