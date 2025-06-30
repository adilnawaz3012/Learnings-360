from typing import List

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        k = 0
        n = len(nums)
        prev = -101
        for idx in range(0, n):
            if prev != nums[idx]:
                nums[k] = nums[idx]
                k += 1
                prev = nums[idx]
        return k