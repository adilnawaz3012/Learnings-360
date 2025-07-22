class Solution:
    def arithmeticTriplets(self, nums: List[int], diff: int) -> int:
        # Since the nums is already strictly increasing, so no need to sort, else perform sorting
        n = len(nums)
        unique_arithmetic_triplets = 0
        """
            - Use 2 pointer to consider indexing
            - no need to track unique triplets as the array is strictly increasing
            - so when we get an answer, we increment j and decrement k, so every time we have new set of index triplets
        """
        for i in range(0, n):
            j = i + 1
            k = n - 1
            while j < k:
                _diff1 = nums[j] - nums[i]
                _diff2 = nums[k] - nums[j]
                if _diff1 == diff and _diff2 == diff:
                    unique_arithmetic_triplets += 1
                    j += 1
                    k -= 1
                elif _diff1 < diff or _diff2 < diff:
                    j += 1
                else:
                    k -= 1
        return unique_arithmetic_triplets
