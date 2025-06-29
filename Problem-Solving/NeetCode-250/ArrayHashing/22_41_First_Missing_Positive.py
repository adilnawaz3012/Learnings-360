from typing import List

class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)

        # 1. Make all negative integer to some positive interger more than n, like n + 1
        for idx, num in enumerate(nums):
            if num <= 0:
                nums[idx] = n + 1
        
        # 2. Mark all integer as negive if num if found, like if num is 3, then mark num - 1 ( 2 ) as -ve
        for idx, num in enumerate(nums):
            _idx = abs(num) - 1
            if 0 <= _idx < n:
                if nums[_idx] >= 0:
                    nums[_idx] *= -1
        
        # 3. Start from first idx, and find which element is +ve, the positive idx ( idx + 1) is the first positive missing number
        for idx, num in enumerate(nums):
            if nums[idx] > 0:
                return idx + 1
        return n + 1