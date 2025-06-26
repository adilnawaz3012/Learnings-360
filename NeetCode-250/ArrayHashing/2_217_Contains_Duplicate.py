from typing import List

from collections import Counter

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        n = len(nums)
        _counter = Counter(nums)
        return True if max(_counter.values()) >= 2 else False