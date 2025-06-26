import heapq
from collections import Counter
from typing import List

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        max_heap = []
        _counter = Counter(nums)
        for key, val in _counter.items():
            heapq.heappush(max_heap, (-val, key))
        result = []
        while k:
            val, key = heapq.heappop(max_heap)
            result.append(key)
            k -= 1
        return result