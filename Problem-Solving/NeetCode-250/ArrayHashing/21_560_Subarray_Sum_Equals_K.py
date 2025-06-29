from typing import List

from collections import Counter

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)

        """
            NOTE:
                The sliding window technique works only when all numbers are non-negative, 
                but here the array contains negative numbers, 
                so the sum can increase or decrease unpredictably.
            
            prefix_sum[j] - prefix_sum[i] = sum(nums[i ... j])
        """
        cumulative_sum_counter = Counter({0: 1})
        count_subarrays = 0
        cumulative_sum = 0

        for num in nums:
            cumulative_sum += num
            count_subarrays += cumulative_sum_counter[cumulative_sum - k]
            cumulative_sum_counter[cumulative_sum] += 1
        return count_subarrays
