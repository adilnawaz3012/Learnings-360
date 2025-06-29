from typing import List

from collections import Counter

class Solution:
    def majorityElement(self, nums: List[int]) -> List[int]:
        _counter = Counter(nums)
        n = len(nums)
        result = []
        for key, val in _counter.items():
            if val > n // 3:
                result.append(key)
        return result