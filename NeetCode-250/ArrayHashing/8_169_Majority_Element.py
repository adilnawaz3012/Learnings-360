from typing import List
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        from collections import Counter
        _counter = Counter(nums)
        n = len(nums)
        for key, val in _counter.items():
            if val > n / 2:
                return key
        return -1